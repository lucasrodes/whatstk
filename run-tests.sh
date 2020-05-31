## (1) Test dependencies (run this part only the first time)

## (1.1) Install pytest dependencies
# pip install -r requirements-test.txt

## (1.2) Install flake8 dependencies
# pip install -r requirements-flake.txt

## (1.3) Generate chats for test
# mkdir -p tests/chats/hformats tests/chats/merge
# whatstk-generate-chats --size 500 --output-path tests/chats/hformats/
# whatstk-generate-chats --size 300 --last-timestamp 2019-09-01 \
#                         --hformats '%Y-%m-%d, %H:%M - %name:' \
#                         --output-path tests/chats/merge/ --filenames file1.txt
# whatstk-generate-chats --size 300 --last-timestamp 2020-01-01 \
#                         --hformats '%Y-%m-%d, %H:%M - %name:' \
#                         --output-path tests/chats/merge/ --filenames file2.txt


## (2) Run flake
flake8 --max-complexity 10 --format=html --docstring-convention=google --htmldir=flake-report whatstk

## (3) Run tests
py.test --html=testreport.html --cov-report html --cov-report term --cov-report xml:cov.xml --cov=whatstk tests/

