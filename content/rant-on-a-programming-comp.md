---
title: The worst programming competition ever
date: 23-11-2023
edited: 31-01-2024
summary: A rant on the worst programming competition I've ever been in.
draft: False
---

On the 18th of November, 2023, I had the opportunity to participate in a high school python programming challenge hosted by a school nearby which was strange considering there hadn't been a competition ever heard of like it over where I live. Most school-based competitions tend to be for art, dancing, or literature so this was a great opportunity given to me by one of the computer science teachers of my school. Without thinking twice, I agreed to participate along with my friend Sam and we were off to go... except for the fact that there was 0 info whatsoever on any sort of guidelines or what to look for in the competition which now, in hindsight, was a huge red flag that I should've recollected in my head multiple times. I had low hopes on the quality of the problems they may ask but nevertheless I felt like it was an opportunity I shouldn't pass up.

Fast forward to when the actual event began, Sam and I sat in front of one of the designated computers in the cramped computer lab, and in a few minutes, the competition was set to begin. The question was:

## Find the longest [substring](https://en.wikipedia.org/wiki/Substring) in a given string without repeating characters

Naturally, like most people (I'd assume), what I felt the question meant was that all we needed was a substring without any repeating characters and could start and end on any position in the string provided it just was the longest substring in the string. So we both came up with a plan that involved looping through each character in the string, beginning counting towards the right until there was a repeating character in the substring, breaking the loop once we found a repeating character. Now this may not sound like the right solution, but hear me out; we weren't even halfway there until 3 other teams suddenly reported that they've completed their code. It looked a little something like this:

```
def substr_longest(text):
    chars = ''
    for char in text:
        if char not in chars:
            chars += char
        else:
            break
    return chars
```

Now at first glance, it seems like this code works. After all, a string like 'abcdaef' should have its longest substring as 'abcd' However, as soon as you input a word like 'helloworld', you'll quickly come to realize the function returns 'hel' while instead the longest substring, without repeating characters, is in fact 'world' which clearly isn't being output by the function above.

As the petty participants we were, we questioned the logic behind this to the event runners over there only for us to receive an unsatisfactory and irrational reply to our questions. They said a substring had to start from the beginning of a string and had to be sequential, which made me question the definition of a substring in the first place. This was totally bogus and my brain further melted into mush when they tried to justify 'hel' being the longest substring in 'helloworld', and so we lost the first round in just 5 minutes. Unfairly. Along with around 5-6 other teams from other schools.

Keeping aside the concern about the inconsistent and nonexistent criteria and guidelines for the competition, what pissed me off was the fact that all the computer science teachers with probably a basic degree or more on the subject got the whole concept of a substring wrong. You simply cannot justify another meaning to this question no matter what way you approach or read in my opinion. In hindsight, I should've clarified what they meant but we both were confident that what we understood was actually right and besides, an hour seemed apt given that it took us a slight bit of time to find an idea to approach and solve the question. Our hearts both sank when we heard the next question was a program [to determine whether a given number was prime or not](https://gist.github.com/simonknowsstuff/2784b48bf0fa27f779ef6f86163abb11) which definitely was the easier one to program compared to this problem.

For those interested, I went ahead and sketched out a solution right below using the logic I mentioned previously:

```
def substr_longest(text):
    longest = ''
    for i in range(len(text)):
        substring = ''
        for char in text[i:]:
            if char not in substring:
                substring += char
            else:
                break
        if len(substring) > len(longest):
            longest = substring
    return longest
```

It's basically a modification of the previous code except over here, we loop through all the characters of the string and break only when there's a repeating character. I'm sure there might be shorter ways to do it, but since this program seems to be tidy enough, I'm keeping it here. I would love to see other approaches to the same problem though! :D