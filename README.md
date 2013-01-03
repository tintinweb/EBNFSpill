EBNFSpill
=========

* Create Random Data based on EBNF Syntax description
* Validate EBNF definition (simpleparse's part)
* Validate some data against EBNF (simpleparse's part)

EBNF-Parser: simpleparse

EBNF-Description
=======

Our simple INI-file looks like this:
[MyFirstSection]
myKey	="myValue9_test-test2"
myKey2	="myValue9_test-test2"
myKey3	="myValue9_test-test2"
myKey4	="myValue9_test-test2"

[MySecond-Section]
myKey11	="myValuexx33_test-test2"


EBNF Declaration for a simple INI-File-Syntax:

	file              := (section, entry+, '\n\n')+
	section           := '[', wordspecial, ']','\n'
	entry             := word, '\t=', '"', wordspecial , '"', '\n'
	alpha             := [a-zA-Z]
	alphanum          := [a-zA-Z0-9]
	alphanumspecial   := [a-zA-Z0-9_-]
	word              := alpha,alphanum*
	wordspecial       := alpha,alphanumspecial*

Description:
'file'           ... our root definition (aka production) which describes the overall file syntax
'section'        ... Ini-file section header
'entry'          ... one key=value entry
'alpha'          ... alpha-chars only
'alphanum'       ... alphanumerical chars
'alphanumspecial'... alphanumerical and _- chars
'word'           ... begins with alpha and continues with none or more alphanums
'wordspecial'    ... begins with alpha and continues with none or more alphanumspecial chars


EBNFSpill Example
=================

EBNFSpill will now take any EBNF defintion that is valid and will try to create random data that matches the described syntax. For the above EBNF declaration this would be random data like this:

	[JaW-I]
	MEk	="RIO_ZC"
	KG1HWR0BcYATBF0CpgS5h	="IzOI5ECekj"
	c8bDI3ozx3LnwnjpM2lz8	="go8iJsKkJ44JI"
	shX3KIJLQkvNEEq1Ja	="E3usLXmAEifbDWOt"
	
	
	[y7aM2A1QIpcThzPRc0ryFU]
	Ng7fMShX4	="Xq"
	d43i42sbool3BnI24e	="t1d5GHD"
	
	
	[EJ4ll]
	NuCG	="J0WrZdTnheSQq"
	Rm6STRGxllBxlf9fLlEmEtwbgH	="cU82WpNkrHR0CqseBltmGOETdf"
	LSadRHDXJ0	="G0Ir0FufaQJdSg9F"
	R5T02vYsf	="JaJaPIUPh0zSSYSM4wfA8pjOq"
	r6zhJQ7K	="GdYp9hMJjA8"
	XMwdm	="wMjUQ0ADRjkT7MPV5zG"
	
	
	[PXj0N0hrfu9e6dKM9-ujmEHuoU]
	d1QFqfbTuqHnVQbK	="wwQ0-sykooiJp201HCwm73fD3"
	fQuzvHP2pVwvS8G7UB6s	="PjofofSqLK4Nv25baoAi_RR7D"
	jtrOtloyXUHJUKe	="k8P3WxPBRbwPrrh0"
	uAuSDmzSVkSHNp0	="MBLM6Lw"
	zEAwWEmfNpt	="ZkecJcD"
	LcOuVkhLGJkCQYbI	="gnj_n8_FE"
	I7TjmZC6	="ci1YzwboZz"
	
	
	[IMw_fjT1jv]
	cIXGM8TQuM29aWnXi9aYK	="UwL_q7RC0JKv7lkFPY"
	mmNGyBCO6qTF2yKvelBki77Wz	="b1UZDdc7vT"
	TPDcJMTv6mMuOKAoNS1xLf	="TSvbaGyW7K5nV"
	aA6qLkQC08	="H3UBl852kRFXlsmoqoX3nO4eGZ"
	z7xPM9YLNOro6FKvc1QqkL6zl	="VwiMf6EdCdK6cG7MtCLdof9h"