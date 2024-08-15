from os import system
from string import digits
import random
from pygetwindow import getActiveWindowTitle
from pynput.keyboard import Listener, Key, KeyCode
from .color import foreground, background

type _key = Key | KeyCode

def clear() -> None:
	system("cls")

class ChoiceInterface:
	def __init__(
		self, *,
		textColor: foreground = foreground.WHITE,
		highlightTextColor: foreground = foreground.BLACK,
		highlightColor: background = background.WHITE,
		confirmKey: list[_key] | tuple[_key, ...] | _key = (Key.enter, Key.right),
		cancelKey: list[_key] | tuple[_key, ...] | _key = Key.esc,
		choicesSurround: str = "",
		addArrowToSelected: bool = False
	) -> None:
		r"""
		Creates the callable ChoiceInterface instance
		:param textColor:
		:param highlightTextColor:
		:param highlightColor:
		:param confirmKey:
		:param cancelKey:
		:param choicesSurround:
		:param addArrowToSelected:
		"""
		cfKey = self.__conv_keys(confirmKey)
		ccKey = self.__conv_keys(cancelKey)
		if set(cfKey) & set(ccKey):
			raise ValueError("values in confirmKey and cancelKey may not overlap!")
		self.confirmKeys = cfKey
		self.cancelKeys = ccKey
		self.textColor = textColor
		self.hlTextColor = highlightTextColor
		self.hlColor = highlightColor
		self.choicesSurround = choicesSurround
		self.addArrowToSelected = addArrowToSelected
		self.terminalWindowTitle = "Choice Interface {" + "".join(random.choices(digits, k=10)) + "}"
		self.lastKeyPressed = None

	@staticmethod
	def __conv_keys(item: tuple[_key, ...] | list[_key] | _key) -> list[_key]:
		if isinstance(item, tuple):
			return list(item)
		elif isinstance(item, list):
			return item
		return [item]

	def __call__(
			self,
			choices: list[str],
			prefix: str = "",
			suffix: str = "",
			selected: int = 0,
			minimumHighlightLength: int = 0,
			terminalTitleBefore: str = "Terminal",
			returnLine: bool = False
		) -> int | tuple[int, str]:
		r"""
		Starts the interface
		:param choices:
		:param prefix:
		:param suffix:
		:param selected:
		:param minimumHighlightLength:
		:param terminalTitleBefore:
		:param returnLine:
		:return:
		"""
		system(f"TITLE {self.terminalWindowTitle}")

		if len(choices) <= 1 or (not (isinstance(choices, list) and all([isinstance(x, str) for x in choices]))):
			raise ValueError("Parameter 'lines' must be of length >= 2 and of type list[str]")
		if 0 > selected >= len(choices):
			raise ValueError(
				"Parameter 'selected' must be index of line in 'lines' and may therefore not be bigger than the "
				"biggest index of 'lines' or smaller than 0"
			)

		if minimumHighlightLength > 0:
			hlLen = minimumHighlightLength
		else:
			hlLen = max([len(line) for line in choices]) + abs(minimumHighlightLength)
			if self.addArrowToSelected:
				hlLen += 3

		while True:
			clear()
			if prefix:
				print(self.textColor.value + prefix + foreground.RESET.value)

			for i, line in enumerate(choices):
				_out = ''
				if i == selected:
					if not any([self.choicesSurround, self.addArrowToSelected]):
						_out = f"{self.hlColor.value+self.hlTextColor.value}{line:<{hlLen}}{foreground.RESET.value}"
					elif self.addArrowToSelected:
						_out = f"{self.hlColor.value+self.hlTextColor.value}{line:<{hlLen-3}} > {foreground.RESET.value}"
					else:
						_out = f"{self.hlColor.value+self.hlTextColor.value}{line:<{hlLen}}{foreground.RESET.value}"
				else:
					_out = f"{self.textColor.value}{line:<{hlLen}}{foreground.RESET.value}"
				if self.choicesSurround:
					_out = self.choicesSurround+_out+self.choicesSurround
				print(_out)

			if suffix:
				print(self.textColor.value+prefix+foreground.RESET.value)

			key: _key | None = self._waitForKey()

			if key == Key.down and selected != len(choices)-1:
				selected += 1
			elif key == Key.up and selected != 0:
				selected -= 1
			elif key in self.confirmKeys:
				if key == Key.enter: input()
				system(f"TITLE {terminalTitleBefore}")
				if returnLine:
					return selected, choices[selected]
				return selected
			elif key in self.cancelKeys:
				if key == Key.enter: input()
				system(f"TITLE {terminalTitleBefore}")
				if returnLine:
					return -1, ""
				return -1
			elif key in [Key.down, Key.up]:
				pass
			else:
				raise Exception("Somehow, Somewhere, Something went wrong :/")

	def _waitForKey(self) -> _key | None:
		lst = Listener(on_press=lambda key: self._onKeyPress(key, lst))
		lst.start()
		lst.join()
		return self.__lastKeyPressed

	def _onKeyPress(self, key: _key | None, lst: Listener) -> None:
		if getActiveWindowTitle() != self.terminalWindowTitle:
			return
		self.__lastKeyPressed = key
		validKeyList: list[_key] = self.confirmKeys+self.cancelKeys+[Key.up, Key.down]
		if self.__lastKeyPressed in validKeyList:
			lst.stop()
