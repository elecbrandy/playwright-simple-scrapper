import os
from typing import List
from playwright.async_api import Browser, Playwright

async def launch_chromium(
		pw: Playwright,
		headless: bool = True,
		extra_args: List[str] = None
	) -> Browser:
	is_ci = os.getenv("CI") or os.getenv("GITHUB_ACTIONS")
	args = [
		"--no-sandbox",							# disable sandboxing
		"--disable-setuid-sandbox",				# disable setuid sandbox
		"--disable-dev-shm-usage",				# disable /dev/shm usage
		"--disable-blink-features=AutomationControlled", # disable automation features
		"--disable-features=TranslateUI",		# disable translation UI
		"--mute-audio",							# mute audio
		"--disable-gpu",						# disable GPU hardware acceleration
		"--disable-extensions",					# disable extensions
		"--disable-background-networking",		# disable background networking
		"--disable-sync",						# disable sync
		"--disable-default-apps",				# disable default apps
		"--no-first-run",						# disable first run UI
	]
	if extra_args:
		args += extra_args
	if is_ci:
		args += ["--single-process"]
	
	# Launch the browser!
	browser = await pw.chromium.launch(headless=headless, args=args)
	return browser

