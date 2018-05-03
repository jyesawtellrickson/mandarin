# Mandarin
An app for learning Mandarin language.

Mandarin is the first fully tailored language learning experience. The main features:
 - Fully customisable content: choose your tastes, like c-pop? learn from lyrics! Interested in Science? read articles! Better than learning books or any teacher and content is updated...daily!
 - Your brain, duplicated: we track everything about your learning process, from the time you took to select an answer to the words you mixed up because they sound the same, and use this to maintain a version of your learning brain and tailor an experience off.
 - One-of-a-kind features: learn new words from the world around you with computer vision, speak to a chatbot.



Working with pinyin and characters:
https://github.com/hermanschaaf/mafan

Chinese word data.
http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0010729
To get sentences containing words, best to use subtitles from children shows or easy dramas / movies.

Character mappings:
http://www.learnm.org/data/adjlist.txt

Learning order:
http://www.learnm.org/data/DNWorder.txt

Chinese gov:
http://www.gov.cn/gzdt/att/att/site1/20130819/tygfhzb.pdf

Chinese dict:
https://github.com/dongxiexidian/Chinese

Pinyin:
https://github.com/hotoo/pinyin

Character decompositions:
https://sourceforge.net/projects/hanzidecomposition/?source=typ_redirect

interesting analysis old hsk vs new.
http://www.zhtoolkit.com/posts/2012/09/mapping-the-old-hsk-onto-new/

learn chinese words with word2vec and then use compression to turn these vectors into 2D. PLot these. Are there any meanings that are focused more in certain levels?

API data source:
https://www.hsk.academy/api/en/hsk/1



HSK word lists
http://www.hskhsk.com/word-lists.html

## Data Sources

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

## To Do
Acquire other learning methods data, e.g. characters from base up
Acquire chinese subtitle data - can we take screencaps as well to link?? :OOO
Train word2vec model on chinese/english to create 'similar' term lists
Map sentences in subtitles to hsk vocab and label accordingly
Decide on 'meaning' of sentence. Thus if a user is interested in a topic we can choose sentences most similar to the topic
Choose an object recognition model
Investigate a model to generate sentences (customized for the user and their vocab / interests) [generating isn't the best option, tagging and using is better]
Map out data tracking for the user history and performance
Create diagrams for UI/UX
Decide on selling points: always new content, image based learning, while you learn so do we
Auto generation of sentences?
Medals for certain topics, e.g. animals, throughout the learning process you fill up the meter for this and when a medal has some progress you can start a topic on that.
Etymology https://www.yellowbridge.com/chinese/character-etymology.php?zi=%E8%A7%81
pull images from google with search / taggings

NLTK
https://github.com/FudanNLP/fnlp/wiki/quicktutorial
