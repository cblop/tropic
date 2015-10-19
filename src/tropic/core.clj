(ns tropic.core
  (:require [instaparse.core :as insta]))

(def inform
  (insta/parser
   "rule = 'Definition: ' ('a ' / 'an ') kind ' is ' adjective (' if ' / ' unless ') definition
    | preamble <': '> phrases
    definition = condition
    | ('its' / 'his' / 'her' / 'their') ' ' property ' ' ('is' / 'are') ' ' value ' or ' ('less' / 'more')
    | ': ' phrases
    preamble = 'To ' word
    | 'To decide ' ('if' / 'whether') ' ' word
    | 'To decide ' ('which' / 'what') ' ' word
    | 'This is the ' word
    phrases = phrase+
    phrase = word | word <' '>
    kind = word
    property = word
    value = word
    condition = word
    adjective = word
    word = #'[0-9a-zA-Z\\-\\_]*'"))

(inform "To exit: go north")
(inform "Definition: a toad is ugly if warty")
(inform "Definition: a toad is dying if its health is 10 or less")


