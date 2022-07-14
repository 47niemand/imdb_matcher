# description

This app is used to match files in a directory to imdb titles. 

# prerequisite

- Python 3.6+
- ```pip3 install imdb-sqlite```
- ```pip3 install transliterate```
- ```pip3 install hachoir```
- ```pip3 install python-Levenshtein-wheels```
- ```pip3 install SQLAlchemy```

# install

```bash
  $ git clone https://github.com/47niemand/imdb_matcher.git imdb_matcher
  $ cd imdb_matcher 
  $ imdb-sqlite
```

# run the program

If meta data available, additional tags will be created. Run this command, which is optional, to generate meta data for video files:

```bash
  $ ./extract_metadata.sh {directory_name}
  
  Processing {directory_name}/{files}.mkv
  ...
```

As result, a file named ```{directory_name}/{files}.info``` will be created, for each video file.

To match files in a directory to imdb titles, run the program with the following command:

```bash
  $ python3 matcher.py {directory_name}
  
  2022-07-14 13:59:17,419 Found 1 files
  2022-07-14 13:59:17,420 Opening database
  2022-07-14 13:59:19,477 Found 351556 titles
  REM ================================================================
  CHCP 65001
  REM # ('thewizardofoz1939', 1.0, 'The Wizard of Oz', 1939, 'tt0032138')
  REN "The Wizard of Oz (1939).mkv" "The_Wizard_of_Oz.(1939).mkv"   
```
