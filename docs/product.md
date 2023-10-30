
## Data Sources

### Dictionary
https://www.mdbg.net/chinese/dictionary?page=cedicttho

### HSK Lists
HSK (Hanyu Shuiping Kaoshi) or the Chinese Proficiency Test is an international standardised exam which tests and rates Chinese language proficiency. It evaluates Chinese language abilities for non-native Chinese speakers in term of using the Chinese language in their daily, academic and professional lives.

Many students learn based off the HSK system which has been specifically designed to help learners pick up the language as quickly as possible. Initially this is the base for the language but eventually this could be changed depending on the goal, e.g. learning Chinese or passing a test.

### Character Decompositions
A basic Chinese character is composed of strokes. These basic characters can be continuously combined to form more complex characters. Character decompositions consist of a character and the two characters which are combined to create it.

### Chinese Questions, English Answers (and reverse)
https://www.plecoforums.com/threads/mnemosyne-20-000-chinese-sentences-hsk-level-1.1846/

### Sentences
Sentences can be used to help with association.
https://tatoeba.org/eng/downloads
Good thread discussing sentences:
https://forum.koohii.com/thread-13204.html

More sentences:
http://hua.umf.maine.edu/China/database.html

#### Preprocessing
To use sentences, there are numerous things we need to do first.
 1. Split sentences into 'words'.
 2. Tag sentences with category tags.
 3. Identify difficulty of sentence (e.g. HSK level, current user vocab)
From the more difficult sentences we can auto-translate the difficult words to make them readable.

### Subtitles Data

#### Screenshots and Audio
Where licensing is available, screenshots and audio should be included.

## Internal Data
As a user interacts with the app, it is expected that the app will learn more about the user and customise the experience.

By tailoring the app as much as possible to the user and combining this with machine generated questions, we can create a unique and personalised experience for the user that is even better than a personal teacher.

### Interests
In time we should collect information on what the user is interested in.

We can ask the user some personalisation questions initially, e.g. are you interested in Chinese Pop / Dramas? Politics? Art? In the format:
 - topic
 - created_at

We can collect feedback on questions.
 - question_id
 - interest
 - difficulty
 - created_at

A user should also be indicating which words they want to learn.
 - word
 - created_at

### Performance Based
The performance of a user should be tracked in order to help them work on tough words, revise forgotten words and pass over known ones. To do this, a database will be maintained with the following parameters:
 - question
 - answers
 - format
 - tested_at
 - answered_at
 - finished_at
 - choice
 - correct

This will allow us to do a few things:
 1. Using the timing we can test as the word is far in the past.
 2. Using the attempt, we can see what the user tried, and judge how close they were to the answer, guiding the next test to show.
 3. By seeing what it was tested with we can alternate and evolve this in time.

## Misceallaneous
### Encodings
Chinese can be quite a bit more difficult to work with.

Some tips for decoding:
http://www.martinaulbach.net/linux/command-line-magic/41-dealing-with-inconsistent-or-corrupt-character-encodings
https://stackoverflow.com/questions/539294/how-do-i-determine-file-encoding-in-osx
chinese: gbk, gb2312, gb18030
