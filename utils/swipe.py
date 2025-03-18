import logging
import logging as log
from typing import Literal, Optional

from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement

from utils import ELEMENT
from utils.driver_commands import DriverCommands


class Swipe:
    def __init__(
        self,
        driver: WebDriver,
        screen_border_x: int = 100,
        screen_border_y: Optional[int] = None,
    ) -> None:
        self.driver = driver
        self.screen_size = self.driver.get_window_size()
        self.dc = DriverCommands(self.driver)
        self.screen_border_x = screen_border_x
        if not screen_border_y:
            self.screen_border_y = self.screen_size.get("height") / 5
        else:
            self.screen_border_y = screen_border_y

    def swipe(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration: int = 1000,
        count: int = 1,
    ) -> None:
        """
        Swipes screen.

        :param start_x: x-coordinate at which to start
        :param start_y: y-coordinate at which to start
        :param end_x: x-coordinate at which to stop
        :param end_y: y-coordinate at which to stop
        :param duration: defines the swipe speed as time taken to swipe
            from point a to point b, in ms.
        :param count: number of swipe repetitions
        """
        for _ in range(count):
            self.driver.swipe(
                start_x=start_x,
                start_y=start_y,
                end_x=end_x,
                end_y=end_y,
                duration=duration,
            )

    def _swipe_in_specified_direction(
        self, direction: Literal["down", "up", "right", "left"], **kwargs: int
    ) -> None:
        """
        Swipes the screen in the specified direction.

        :param direction: the direction to swipe, must be one of:
            - 'up'
            - 'down'
            - 'left'
            - 'right'
        :keyword start_x: x-coordinate to start the swipe. Defaults to the center of the screen
        :keyword start_y: y-coordinate to start the swipe. Defaults to the center of the screen
        :keyword end_x: x-coordinate to stop the swipe. Defaults to the center of the screen
        :keyword end_y: y-coordinate to stop the swipe. Defaults to the center of the screen
        :keyword duration: the duration of the swipe in milliseconds, defaults to 1000ms
        :keyword count: the number of times to repeat the swipe, defaults to 1
        """
        log.info(f"Swiping {direction}")
        start_x = kwargs.get("start_x") or (self.screen_size["width"] / 2)
        start_y = kwargs.get("start_y") or (self.screen_size["height"] / 2)
        end_x = kwargs.get("end_x") or (self.screen_size["width"] / 2)
        end_y = kwargs.get("end_y") or (self.screen_size["height"] / 2)
        match direction:
            case "down":
                end_y = kwargs.get("end_y") or self.screen_border_y
            case "up":
                end_y = kwargs.get("end_y") or (self.screen_size["height"] - self.screen_border_y)
            case "right":
                start_x = kwargs.get("start_x") or self.screen_border_x
                end_x = kwargs.get("end_x") or (self.screen_size["width"] - self.screen_border_x)
            case "left":
                start_x = kwargs.get("start_x") or (
                    self.screen_size["width"] - self.screen_border_x
                )
                end_x = kwargs.get("end_x") or self.screen_border_x
        duration = kwargs.get("duration") or 1000
        count = kwargs.get("count") or 1
        self.swipe(
            start_x=start_x,
            start_y=start_y,
            end_x=end_x,
            end_y=end_y,
            duration=duration,
            count=count,
        )

    def swipe_down(self, **kwargs: int) -> None:
        """
        Swipes screen down.

        :keyword start_x: x-coordinate to start the swipe. Defaults to the center of the screen
        :keyword start_y: y-coordinate to start the swipe. Defaults to the center of the screen
        :keyword end_x: x-coordinate to stop the swipe. Defaults to the center of the screen
        :keyword end_y: y-coordinate to stop the swipe. Defaults to the center of the screen
        :keyword duration: the duration of the swipe in milliseconds, defaults to 1000ms
        :keyword count: the number of times to repeat the swipe, defaults to 1
        """
        self._swipe_in_specified_direction("down", **kwargs)

    def swipe_up(self, **kwargs: int) -> None:
        """
        Swipes screen up.

        :keyword start_x: x-coordinate to start the swipe. Defaults to the center of the screen
        :keyword start_y: y-coordinate to start the swipe. Defaults to the center of the screen
        :keyword end_x: x-coordinate to stop the swipe. Defaults to the center of the screen
        :keyword end_y: y-coordinate to stop the swipe. Defaults to the center of the screen
        :keyword duration: the duration of the swipe in milliseconds, defaults to 1000ms
        :keyword count: the number of times to repeat the swipe, defaults to 1
        """
        self._swipe_in_specified_direction("up", **kwargs)

    def swipe_right(self, **kwargs: int) -> None:
        """
        Swipes screen right.

        :keyword start_x: x-coordinate to start the swipe. Defaults to the center of the screen
        :keyword start_y: y-coordinate to start the swipe. Defaults to the center of the screen
        :keyword end_x: x-coordinate to stop the swipe. Defaults to the center of the screen
        :keyword end_y: y-coordinate to stop the swipe. Defaults to the center of the screen
        :keyword duration: the duration of the swipe in milliseconds, defaults to 1000ms
        :keyword count: the number of times to repeat the swipe, defaults to 1
        """
        self._swipe_in_specified_direction("right", **kwargs)

    def swipe_left(self, **kwargs: int) -> None:
        """
        Swipes screen left.

        :keyword start_x: x-coordinate to start the swipe. Defaults to the center of the screen
        :keyword start_y: y-coordinate to start the swipe. Defaults to the center of the screen
        :keyword end_x: x-coordinate to stop the swipe. Defaults to the center of the screen
        :keyword end_y: y-coordinate to stop the swipe. Defaults to the center of the screen
        :keyword duration: the duration of the swipe in milliseconds, defaults to 1000ms
        :keyword count: the number of times to repeat the swipe, defaults to 1
        """
        self._swipe_in_specified_direction("left", **kwargs)

    def swipe_to_object_down(
        self,
        my_object: ELEMENT,
        max_count_of_swipe: int = 10,
        duration: Optional[int] = 1000,
    ) -> WebElement:
        """
        Swipes down until element is visible on the screen.

        :param my_object: element to swipe to
        :param max_count_of_swipe: maximum count of swipes
        :param duration: defines the swipe speed as time taken to swipe
        :return: WebElement
        """
        return self._swipe_direction_to_object(
            direction="down",
            my_object=my_object,
            duration=duration,
            max_count_of_swipe=max_count_of_swipe,
        )

    def swipe_to_object_up(
        self,
        my_object: ELEMENT,
        max_count_of_swipe: int = 10,
        duration: Optional[int] = 1000,
    ) -> WebElement:
        """
        Swipes up until element is visible on the screen.

        :param my_object: element to swipe to
        :param max_count_of_swipe: maximum count of swipes
        :param duration: defines the swipe speed as time taken to swipe
        :return: WebElement
        """
        return self._swipe_direction_to_object(
            direction="up",
            my_object=my_object,
            duration=duration,
            max_count_of_swipe=max_count_of_swipe,
        )

    def _swipe_direction_to_object(
        self,
        direction: Literal["up", "right", "left", "down"],
        my_object: ELEMENT,
        duration: Optional[int],
        max_count_of_swipe: int = 10,
    ) -> WebElement:
        """
        Swipes in the specified direction until the element is visible on the screen,
        this method performs repeated swipes in the given direction until the specified
        element becomes visible or the maximum number of swipes is reached.

        :param direction: the direction to swipe, must be one of:
            - 'up'
            - 'down'
            - 'left'
            - 'right'
        :param my_object: the element to swipe to
        :param duration: the duration of each swipe in milliseconds
        :param max_count_of_swipe: the maximum number of swipes to perform, defaults to 10
        :returns: the found element if it becomes visible within the maximum number of swipes
        """
        if isinstance(my_object, str):
            my_object = self.dc.convert_selector(my_object)
        for i in range(max_count_of_swipe):
            element = self.dc.find_elements(my_object)
            if element and element[0].is_displayed():
                logging.info(
                    f"Element {my_object} found after {i}"
                    f" swipes to {direction}. ID: {element[0].id}"
                )
                return element[0]
            else:
                log.info(f"Element {my_object} not visible. Swiping {direction}.")
                match direction:
                    case "up":
                        self.swipe_up(duration=duration)
                    case "down":
                        self.swipe_down(duration=duration)
                    case "left":
                        self.swipe_left(duration=duration)
                    case "right":
                        self.swipe_right(duration=duration)
        assert False, f"{my_object} not found after {max_count_of_swipe} swipes to {direction}"
