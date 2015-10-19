(ns tropic.core
  (:require [instaparse.core :as insta]))

(def inform
  (insta/parser
   "rule =
        <'Definition: ' ('a ' / 'an ')> kind <' is '> adjective <' '> ('if' / 'unless') <' '> definition
        | preamble <': '> phrases

    definition =
        condition
        | <('its' / 'his' / 'her' / 'their') ' '> property <' ' ('is' / 'are') ' '> value <' '> 'or' <' '> ('less' / 'more')
        | ': ' phrases

    preamble =
        'To' <' '> phrases
        | 'To decide ' ('if' / 'whether') ' ' phrases
        | 'To decide ' ('which' / 'what') ' ' phrases
        | 'This is the ' word

    circumstances =
        'At ' time
        | 'When ' event
        | [placement] rulebook-reference [' while ' / ' when ' condition] [' during ' scene]

    rulebook-reference =
        word

    placement =
        ('a' / 'an')
        | ['the '] 'first'
        | ['the '] 'last'

    scene =
        word

    phrases = phrase+
    phrase = word | word <' '>
    kind = word
    time = word
    event = word
    property = word
    value = word
    condition = word
    adjective = word
    word = #'[0-9a-zA-Z\\-\\_\\.]*'"))

;; (inform "To exit: go north")
;; (inform "Definition: a toad is ugly if warty")
;; (inform "Definition: a toad is dying if its health is 10 or less")


