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
   "object = (label <' is a ' / ' is an '> type <'.'>? <'\\n'?>)+ <'\\n'?>
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
   "trope = (tropedef (<whitespace> (situationdef / alias / sequence))+ <'\\n'?>) | ((situationdef / alias / sequence)+ <'\\n'?>)

    <tropedef> = label <' is a ' ('trope' / 'policy') ' where:\\n'>

    alias =
        (character <' is also '> character <'\\n'?>) | (object <' is '> object <'\\n'?>)

    situation =
        <'When '> event <':'>

    conditional =
        <'If ' | 'if '> (fluent / tverb / character <' '> (bverb / cverb)) <':'> outcome

    fluent =
        object <' is '> adjective

    adjective = word

    object = name

    outcome =
        (<'\\n' whitespace whitespace> (event | obligation | happens) or? <'\\n'?>)+

    happens =
       <the?> subtrope <(' happens' / ' policy applies') '.'?>


    block =
       <the?> subtrope <' policy does not apply' / ' does not happen'> <'.'?>


    sequence =
        ((conditional | event | norms | happens | block)  <'\\n'?>) | ((conditional | event | norms | happens | block) (<'\\n' whitespace+ 'Then '> (block / conditional / event / obligation / happens) or?))*

    situationdef = situation (<'\\n'> <whitespace> norms | <'\\n'> <whitespace whitespace> consequence)+ <'\\n'?>

    or =
        <'\\n' whitespace+ 'Or '> event


    event =
        (character <' is'>? <' '> (move / task)) | give | sell | tverb | meet | kill | pay


    give =
        character <' gives ' ('the ' / 'a ' / 'an ')?> item <' to '>? <'a ' / 'an '>? character

    sell =
        character <' sells ' ('the ' / 'a ' / 'an ')?> item <' to '>? <'a ' / 'an '>? character

    tverb =
        character <' '> verb <(' the ' / ' a ' / ' an ')?> item <' to '>? <'a ' / 'an '>? character

    bverb =
        verb <(' the ' / ' a ' / ' an ')?> item <' to '>? <'a ' / 'an '>? character

    cverb =
        words <' the ' / ' a ' / ' an '> (object / character)

    meet =
        character <' meets '> character
    kill =
        character <' kills '> character
    pay =
        <'pay '> character

    norms = permission | obligation

    violation = norms

    character = name

    subtrope = <'\"'> words <'\"'>

    label = <'\"'> words <'\"'>

    move = mverb <' '> <'to '?> place
    mverb = 'go' / 'goes' / 'leave' / 'leaves' / ('return' <!' the'>) / 'returns' <!' the'> / 'at' / 'come' / 'comes'
    verb = word
    place = name

    <pverb> = verb (<' '> verb)*

    permission = character <' may '> (move / pay / bverb / cverb / task) conditional? <'\\n'?>
    obligation = character <' must '> (move / pay / bverb / cverb / pverb / task) (<' before '> deadline)? (<'\\n' whitespace+ 'Otherwise, '> <'the '?> violation)? <'.'?> <'\\n'?>

    deadline = consequence

    task = pverb <' '> role-b / verb / (verb <(' the ' / ' a ' / ' an ')> item) / (verb <' '> item)
    role-b = name

    pverb = 'kill' / 'kills' / 'refunds' / 'refund'

    consequence =
        [<'The ' / 'the '>] character <' will '>? <' '> (move / item)
        | [<'The ' / 'the '>] item <' '> verb

    item = [<'The ' / 'the '>] word

    <whitespace> = #'\\s\\s'

    <name> = (<'The ' | 'the '>)? cwords
    <words> = word (<' '> word)*
    <cwords> = cword (<' '> cword)*
    <cword> = #'[A-Z][0-9a-zA-Z\\-\\_\\']*'
    <the> = <'The ' | 'the '>
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
