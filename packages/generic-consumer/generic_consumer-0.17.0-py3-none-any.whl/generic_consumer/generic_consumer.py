from abc import ABC
from logging import Logger
import re
from signal import SIGABRT
from time import perf_counter
from typing import (
    Any,
    Callable,
    Generator,
    Iterable,
    List,
    Optional,
    Tuple,
    Type,
    final,
)
from fun_things import get_all_descendant_classes, categorizer
import fun_things.logger
from simple_chalk import chalk
from .strings import *
from .logger import logger


class GenericConsumer(ABC):
    enabled = True
    """
    If this consumer is enabled.
    """
    log = True
    """
    If the consumer should print logs.
    """
    process_empty_payloads = False
    """
    If the consumer should still process
    even if there are no payloads.

    `process_one` will not be called
    even if this is `True`.
    """
    __run_count = 0

    @final
    def init(self):
        """
        Called when `run()` is called.
        """
        pass

    @classmethod
    @final
    def get_run_count(cls):
        """
        The amount of times this consumer has run.
        """
        return cls.__run_count

    @classmethod
    def passive(cls):
        """
        Determines the consumer's significance in `start()`.

        See `start()` for more details.
        """
        return False

    @classmethod
    def hidden(cls):
        """
        If this consumer should not be displayed when printing
        available consumers.

        Hidden consumers are still called
        if they have a satisfied condition.

        You can override this by making a static/class method
        with the name `hidden`.
        """
        return False

    @classmethod
    def max_run_count(cls):
        """
        The number of times this consumer can be called.

        At 0 or less,
        this consumer can be called at any number of times.

        You can override this by making a static/class method
        with the name `run_once`.
        """
        return 0

    @classmethod
    def queue_name(cls):
        """
        The name of this consumer.

        You can override this by making a static/class method
        with the name `queue_name`.
        """
        return re.sub(
            # 1;
            # Look for an uppercase after a lowercase.
            # HelloWorld = HELLO_WORLD
            # 2;
            # Look for an uppercase followed by a lowercase,
            # after an uppercase or a number.
            # Example; HELLOWorld = HELLO_WORLD
            # 3;
            # Look for a number after a letter.
            # Example; HelloWorld1 = HELLO_WORLD_1
            r"(?<=[a-z])(?=[A-Z0-9])|(?<=[A-Z0-9])(?=[A-Z][a-z])|(?<=[A-Za-z])(?=\d)",
            "_",
            cls.__name__,
        ).upper()

    @classmethod
    def priority_number(cls):
        """
        If there are multiple consumers that
        have satisfied conditions,
        the highest priority number goes first.

        You can override this by making a static/class method
        with the name `priority_number`.
        """
        return 0

    @classmethod
    def condition(cls, queue_name: str):
        """
        Must return `True` in order for this consumer to be selected.

        By default, this checks if the `queue_name` is the same
        as this consumer's `queue_name`.

        You can override this by making a static/class method
        with the name `condition`.
        """
        return cls.queue_name() == queue_name

    def get_payloads(self):  # type: ignore
        """
        Return the payloads here.

        Can be non-iterable,
        which becomes an array with a single value.
        """
        pass

    def payload_preprocessors(
        self,
    ) -> Iterable[Callable]:
        """
        Transforms payloads before being processed.
        """
        return []

    @final
    def __preprocess_payload(self, payload):
        processed_payload = payload

        try:
            for processor in self.payload_preprocessors():
                processed_payload = processor(processed_payload)

            return processed_payload
        except Exception as e:
            if self.log:
                logger.error(ERROR_PAYLOAD, e)

        return payload

    @final
    def __preprocess_payloads(self, payloads):
        if not isinstance(payloads, Iterable):
            return [self.__preprocess_payload(payloads)]

        return [*map(self.__preprocess_payload, payloads)]

    def process(self, payloads: list):
        """
        Processes all of the payloads.
        """
        return SIGABRT

    def process_one(self, payload):
        """
        Processes payloads 1 by 1.

        Return `signal.SIGABRT` to stop.
        """
        return SIGABRT

    @final
    def run_all(self, *args, **kwargs):
        return [*self.run(*args, **kwargs)]

    @final
    def __run(self, *args, **kwargs) -> Generator[Any, Any, None]:
        queue_name = self.queue_name()

        self.__class__.__run_count += 1
        self.args = args
        self.kwargs = kwargs

        self.init()

        payloads = self.get_payloads()
        payloads = self.__preprocess_payloads(payloads)
        payloads_count = len(payloads)

        if not self.process_empty_payloads and payloads_count == 0:
            return

        if self.log and payloads_count > 0:
            logger.info(
                INFO_PAYLOAD.format(
                    count=payloads_count,
                    queue_name=queue_name,
                )
            )

        for payload in payloads:
            result = self.process_one(payload)

            if result == SIGABRT:
                break

            yield result

        result = self.process(payloads)

        if result != SIGABRT:
            yield result
            return

    @final
    def run(self, *args, **kwargs):
        """
        Ignores `max_run_count`.
        """
        queue_name = self.queue_name()

        logger.debug(
            INFO_CONSUMER_START.format(
                queue_name=queue_name,
            ),
        )

        t1 = perf_counter()

        for result in self.__run(*args, **kwargs):
            yield result

        t2 = perf_counter()

        logger.debug(
            INFO_CONSUMER_END.format(
                queue_name=queue_name,
                duration=t2 - t1,
            )
        )

    @staticmethod
    @final
    def __consumer_predicate(consumer: Type["GenericConsumer"]):
        max_run_count = consumer.max_run_count()

        if max_run_count <= 0:
            return True

        return consumer.__run_count < max_run_count

    @classmethod
    @final
    def available_consumers(cls):
        """
        All consumers sorted by highest priority number.
        """
        descendants = get_all_descendant_classes(
            cls,
            exclude=[ABC],
        )
        descendants = filter(
            GenericConsumer.__consumer_predicate,
            descendants,
        )

        return sorted(
            descendants,
            key=lambda descendant: descendant.priority_number(),
            reverse=True,
        )

    @classmethod
    @final
    def get_consumer(cls, queue_name: str):
        """
        Returns the first consumer with the given `queue_name`
        and the highest priority number.
        """
        descendants = cls.get_consumers(queue_name)

        for descendant in descendants:
            return descendant

    @classmethod
    @final
    def get_consumers(cls, queue_name: str):
        """
        Returns all consumers that has a
        satisfied `condition(queue_name)`,
        starting from the highest priority number.

        The consumers are instantiated while generating.
        """
        descendants = GenericConsumer.available_consumers()

        for descendant in descendants:
            if not descendant.enabled:
                continue

            if not descendant.condition(queue_name):
                continue

            yield descendant()

    @classmethod
    @final
    def start_all(
        cls,
        queue_name: str,
        print_consumers=True,
        print_indent=2,
        require_non_passive_consumer=True,
    ):
        return [
            *cls.start(
                queue_name,
                print_consumers,
                print_indent,
                require_non_passive_consumer,
            )
        ]

    @classmethod
    @final
    def start(
        cls,
        queue_name: str,
        print_consumers=True,
        print_indent=2,
        require_non_passive_consumer=True,
    ):
        """
        Requires at least 1 non-passive consumer to be selected.
        """
        consumers = [*cls.get_consumers(queue_name)]
        has_non_passive = map(
            lambda v: not v.passive(),
            consumers,
        )
        has_non_passive = any(has_non_passive)

        if print_consumers:
            cls.print_available_consumers(
                queue_name,
                print_indent,
            )
            cls.__print_load_order(consumers)

        if require_non_passive_consumer and not has_non_passive:
            raise Exception(
                ERROR_NO_ACTIVE_CONSUMER.format(
                    queue_name=queue_name,
                ),
            )

        for consumer in consumers:
            queue_name = consumer.queue_name()

            if not consumer.enabled:
                logger.debug(
                    WARN_CONSUMER_DISABLED.format(
                        queue_name=queue_name,
                    ),
                )
                continue

            for result in consumer.run():
                yield result

    @staticmethod
    @final
    def __print_load_order(consumers: List["GenericConsumer"]):
        if not any(consumers):
            return

        print(
            f"<{chalk.yellow('Load Order')}>",
            chalk.yellow.bold("↓"),
        )

        items = map(
            lambda consumer: (
                consumer.priority_number(),
                consumer.queue_name(),
                consumer.passive(),
            ),
            consumers,
        )

        has_negative = consumers[-1].priority_number() < 0
        zfill = map(
            lambda consumer: consumer.priority_number(),
            consumers,
        )
        zfill = map(lambda number: len(str(abs(number))), zfill)
        zfill = max(zfill)

        if has_negative:
            zfill += 1

        for priority_number, queue_name, passive in items:
            if has_negative:
                priority_number = "%+d" % priority_number
            else:
                priority_number = str(priority_number)

            priority_number = priority_number.zfill(zfill)

            if passive:
                queue_name = chalk.blue.bold(queue_name)
            else:
                queue_name = chalk.green.bold(queue_name)

            print(
                f"[{chalk.yellow(priority_number)}]",
                chalk.green(queue_name),
            )

        print()

    @staticmethod
    @final
    def __get_printed_queue_name(
        item: Type["GenericConsumer"],
        queue_name: Optional[str],
    ):
        text = item.queue_name()

        if queue_name == None:
            return text

        if not item.enabled:
            # Not enabled.
            text = chalk.dim.gray(text)
            text = f"{text} {chalk.bold('✕')}"

        elif not item.condition(queue_name):
            # Enabled, but condition is not met.
            text = chalk.dim.gray(text)

        elif item.passive():
            # Passive consumer.
            text = chalk.blue.bold(text)
            text = f"{text} {chalk.bold('✓')}"

        else:
            # Non-passive (active) consumer.
            text = chalk.green.bold(text)
            text = f"{text} {chalk.bold('✓')}"

        return text

    @staticmethod
    @final
    def __draw_consumers(
        queue_name: str,
        consumers: List[Type["GenericConsumer"]],
        indent_text: str,
    ):
        consumers.sort(
            key=lambda consumer: consumer.priority_number(),
            reverse=True,
        )

        count = len(consumers)
        priority_numbers = [
            *map(
                lambda consumer: consumer.priority_number(),
                consumers,
            )
        ]
        max_priority_len = map(
            lambda number: len(str(abs(number))),
            priority_numbers,
        )
        max_priority_len = max(max_priority_len)
        has_negative = map(
            lambda number: number < 0,
            priority_numbers,
        )
        has_negative = any(has_negative)

        if has_negative:
            max_priority_len += 1

        for consumer in consumers:
            count -= 1

            priority_number = consumer.priority_number()

            if has_negative:
                priority_number = "%+d" % priority_number
            else:
                priority_number = str(priority_number)

            priority_number = priority_number.zfill(
                max_priority_len,
            )
            line = "├" if count > 0 else "└"

            print(
                f"{indent_text}{line}",
                f"[{chalk.yellow(priority_number)}]",
                GenericConsumer.__get_printed_queue_name(
                    consumer,
                    queue_name,
                ),
            )

        print()

    @staticmethod
    @final
    def __draw_categories(
        queue_name: str,
        indent_size: int,
        indent_scale: int,
        keyword: str,
        category: Any,
    ):
        if keyword == None:
            keyword = "*"

        indent_text = " " * indent_size * indent_scale

        print(f"{indent_text}{chalk.yellow(keyword)}:")

        if isinstance(category, list):
            GenericConsumer.__draw_consumers(
                queue_name=queue_name,
                consumers=category,
                indent_text=indent_text,
            )
            return

        for sub_category in category.items():
            yield indent_size + 1, sub_category

    @classmethod
    @final
    def print_available_consumers(
        cls,
        queue_name: str = None,  # type: ignore
        indent: int = 2,
    ):
        consumers = filter(
            lambda consumer: not consumer.hidden(),
            cls.available_consumers(),
        )
        categorized: List[Tuple[int, Tuple[str, Any]]] = list(
            map(
                lambda consumer: (0, consumer),
                categorizer(
                    consumers,
                    lambda consumer: consumer.queue_name(),
                ).items(),
            )
        )

        while len(categorized) > 0:
            indent_size, (keyword, category) = categorized.pop()

            sub_categories = GenericConsumer.__draw_categories(
                queue_name=queue_name,
                indent_size=indent_size,
                indent_scale=indent,
                keyword=keyword,
                category=category,
            )

            for sub_category in sub_categories:
                categorized.append(sub_category)
