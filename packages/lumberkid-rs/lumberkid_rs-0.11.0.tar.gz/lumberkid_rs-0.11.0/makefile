version:
	semantic-release version

publish:
	source .env && maturin publish

install-from-pypi:
	pipx upgrade lumberkid-rs

release:
	make version
	make publish
	make install-from-pypi