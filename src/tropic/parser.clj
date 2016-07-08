(ns tropic.parser
  (:require [instaparse.core :as insta]))

(def char-parser
  (insta/parser
   "character = (<'The ' / 'the '>? label <' is a '> role <'.'>? <'\\n'?>)+ <'\\n'?>
    label = words
    role = words
    <words> = word (<' '> word)*
    <word> = #'[0-9a-zA-Z\\-\\_\\']*'"))

(def object-parser
  (insta/parser
   "object = (label <' is a '> type <'.'>? <'\\n'?>)+ <'\\n'?>
    label = words
    type = words
    <words> = word (<' '> word)*
    <word> = #'[0-9a-zA-Z\\-\\_\\']*'"))

(def place-parser
  (insta/parser
   "place = (<'The ' / 'the '>? label <' is ' 'a '?> location <'.'>? <'\\n'?>)+ <'\\n'?>
    label = words
    location = words
    <words> = word (<' '> word)*
    <word> = #'[0-9a-zA-Z\\-\\_\\']*'"))

(def trope-parser
  (insta/parser
   "trope = (tropedef (<whitespace> (situationdef / alias / happens / norms / sequence / situationdef))+ <'\\n'?>) | ((situationdef / alias / happens / norms / sequence / situationdef)+ <'\\n'?>)

    <tropedef> = label <' is a trope where:\\n'>
    alias =
        <whitespace> character <' is also '> character <'\\n'?>

    situation =
        <'When '> event <':'>

    happens =
       <'The ' | 'the '>? subtrope <' happens' '.'?>

    sequence =
        (<whitespace>? <'Then '>? (event | obligation | happens) or? <'\\n'?>)+

    situationdef = situation (<'\\n'> <whitespace> norms | <'\\n'> <whitespace whitespace> consequence)+ <'\\n'?>

    or =
        <'\\n' whitespace+ 'Or '> event


    event =
        (character <' is'>? <' '> (move / task)) | give | meet | kill


    give =
        character <' gives '> character <' a ' / ' an '?> item
    meet =
        character <' meets '> character
    kill =
        character <' kills '> character

    norms = permission | obligation

    violation = norms

    character = name

    subtrope = name

    label = words

    conditional =
        <' if '> <'they '?> event

    move = mverb <' '> <'to '?> place
    mverb = 'go' / 'goes' / 'leave' / 'leaves' / 'return' / 'returns' / 'at' / 'come' / 'comes'
    verb = word
    place = name


    permission = character <' may '> (move / task) conditional? <'\\n'?>
    obligation = character <' must '> (move / task) (<' before '> deadline)? (<'\\n' whitespace+ 'Otherwise, '> <'the '?> violation)? <'.'?> <'\\n'?>

    deadline = consequence

    task = pverb <' '> role-b / verb / (verb <(' the ' / ' a ' / ' an ')> item) / (verb <' '> item)
    role-b = name

    pverb = 'kill' / 'kills'

    consequence =
        [<'The ' / 'the '>] character <' will '>? <' '> (move / item)
        | [<'The ' / 'the '>] item <' '> verb

    item = [<'The ' / 'the '>] word

    <whitespace> = #'\\s\\s'

    <name> = (<'The ' | 'the '>)? cword
    <words> = word (<' '> word)*
    <cwords> = cword (<' '> cword)*
    <cword> = #'[A-Z][0-9a-zA-Z\\-\\_\\']*'
    <word> = #'[0-9a-zA-Z\\-\\_\\']*'"
   ))

(defn parse-trope
  [text]
  (insta/add-line-and-column-info-to-metadata
   text
   (trope-parser text)))

(defn parse-char
  [text]
  (insta/add-line-and-column-info-to-metadata
   text
   (char-parser text)))

(defn parse-object
  [text]
  (insta/add-line-and-column-info-to-metadata
   text
   (object-parser text)))

(defn parse-place
  [text]
  (insta/add-line-and-column-info-to-metadata
   text
   (place-parser text)))
