(ns tropic.parser
  (:require [instaparse.core :as insta]
            [tropic.gen :refer [make-defs-map]]))

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

(def def-parser
  (insta/parser
   "text = tropedef defs trope
    <tropedef> = label <' is a ' ('trope' / 'policy') ' where:\\n'>
    <defs> = (<whitespace> (chardef | objdef | placedef) <'\\n'?>)+
    chardef = charname <' is a ' ('character' | 'role') '.'?>
    objdef = objname <' is an object' '.'?>
    placedef = placename <' is a place' '.'?>
    <charname> = name
    <objname> = name
    <placename> = name
    trope = (<whitespace> !(chardef | objdef | placedef) #'.*' <'\\n'>?)+
    label = <'\"'> words <'\"'>
    <whitespace> = #'\\s\\s'
    <name> = [<'The ' / 'the '>] cwords
    <words> = word (<' '> word)*
    <cwords> = cword (<' '> ['of'<' '>] cword)*
    <cword> = #'[A-Z][0-9a-zA-Z\\-\\_\\']*'
    <the> = <'The ' | 'the '>
    <word> = #'[0-9a-zA-Z\\-\\_\\']*'
"
))

(defn make-pstring [choices]
  (apply str (interpose " | " (map #(str (if (or (= (apply str (take 4 %)) "The ") (= (apply str (take 4 %)) "the ")) (str "<the?> " "'" (apply str (drop 4 %)) "'") (str "'" % "'"))) choices)))
  )

(defn trope-parser-fn [{:keys [label roles objects places]}]
  (let [rs (make-pstring roles)
        os (make-pstring objects)
        ps (make-pstring places)
        ]
    (insta/parser
     (apply str
      (interpose "\n"
                 [
                  "trope = (<whitespace> sequence)+ <'\\n'?>"
                  (str "label = '" label "'")
                  "fluent = object <' is '> adjective"
                  "adjective = word"
                  "outcome =
          (<'\\n' whitespace whitespace> (event | obligation | happens) (or? | if?) <'\\n'?>)+"
                  "happens =
         <the?> subtrope <(' happens' / ' trope happens' / ' policy applies') '.'?>"
                  "block =
         <the?> subtrope <' policy does not apply' / ' does not happen' / ' trope does not happen'> <'.'?>"
                  "sequence =
         ((fluent | event | norms | happens | block) (or* | if*)) | ((fluent | event | norms | happens | block) (<whitespace+ 'Then '> (block / norms / event / fluent / obligation / happens) (or* | if*))*)*"
                  "or =
         <whitespace+ 'Or '> (fluent | event | norms)"
                  "if =
         <whitespace+ 'If '> (fluent | event | norms)"
                  "action = !fverb verb [sp [particle sp] (character | object | place)] (crlf? | [sp particle? (character | object | place)] crlf?)"
                  "event = character sp action"
                  "<particle> = <'a' | 'at' | 'will' | 'of' | 'to'>"
                  "norms = permission | rempermission | obligation"
                  "fluent = (character | object | place) sp fverb sp [particle sp] (character | object | place) crlf?"
                  "fverb = (<'is'> sp 'at') | 'has'"
                  "violation = norms"
                  (str "character = " (if (seq rs) rs "'nil'"))
                  (str "place = " (if (seq ps) ps "'nil'"))
                  (str "object = " (if (seq os) os "'nil'"))
                  "subtrope = <'\"'> words <'\"'>"
                  "label = <'\"'> words <'\"'>"
                  "verb = words"
                  "rempermission = character <' may not '> action crlf?"
                  "permission = character <' may '> action crlf?"
                  "obligation = character <' must '> action (<' before '> deadline)? (<crlf whitespace+ 'Otherwise, '> <'the '?> violation)? <'.'?> crlf?"
                  "deadline = consequence"
                  "role-b = character"
                  "object-b = object"
                  "place-b = place"
                  "<crlf> = <'\\n'>"
                  "consequence = event"
                  "<whitespace> = #'\\s\\s'"
                  "<sp> = <' '>"
                  "<words> = word (sp word)*"
                  "<cwords> = cword (sp ['of' sp] cword)*"
                  "<cword> = #'[A-Z][0-9a-zA-Z\\-\\_\\']*'"
                  "<the> = <'The ' | 'the '>"
                  "<word> = #'[0-9a-zA-Z\\-\\_\\']*'"
                  ])
      ))))

(def trope-parser
  (insta/parser
   "trope = (tropedef (<whitespace> (situationdef / alias / sequence))+ <'\\n'?>) | ((situationdef / alias / sequence)+ <'\\n'?>)

    <tropedef> = label <' is a ' ('trope' / 'policy') ' where:\\n'>

    alias =
        (character <' is also '> character <'\\n'?>) | (object <' is '> object <'\\n'?>)

    situation =
        <'When '> event <':'>

    fluent =
        object <' is '> adjective

    adjective = word

    object = name

    outcome =
        (<'\\n' whitespace whitespace> (event | obligation | happens) (or? | if?) <'\\n'?>)+

    happens =
       <the?> subtrope <(' happens' / ' policy applies') '.'?>


    block =
       <the?> subtrope <' policy does not apply' / ' does not happen'> <'.'?>


    sequence =
        ((event | norms | happens | block)  <'\\n'?> (or* | if*)) | ((event | norms | happens | block) (<'\\n' whitespace+ 'Then '> (block / norms / event / obligation / happens) (or* | if*))*)*

    situationdef = situation (<'\\n'> <whitespace> norms | <'\\n'> <whitespace whitespace> consequence)+ <'\\n'?>

    or =
        <'\\n' whitespace+ 'Or '> (event | norms)

    if =
        <'\\n' whitespace+ 'If '> (event | norms)

    event =
        (<'The '>? character <' is'>? <' '> (move / task)) / give / sell / tverb / meet / kill / pay


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
        (character <' kills '> character) | (character <' may kill '> character)
    pay =
        <'pay '> character

    norms = permission | rempermission | obligation

    violation = norms

    character = name

    subtrope = <'\"'> words <'\"'>

    label = <'\"'> words <'\"'>

    move = mverb <' '> <'to '?> place
    mverb = 'go' / 'goes' / 'leave' / 'leaves' / ('return' <!' the'>) / 'returns' <!' the'> / 'at' / 'come' / 'comes'
    verb = word
    place = name

    <pverb> = verb (<' '> verb)*

    rempermission = character <' may not '> (move / pay / bverb / cverb / task) <'\\n'?>
    permission = character <' may '> (move / pay / bverb / cverb / task) <'\\n'?>
    obligation = character <' must '> (move / pay / bverb / cverb / pverb / task) (<' before '> deadline)? (<'\\n' whitespace+ 'Otherwise, '> <'the '?> violation)? <'.'?> <'\\n'?>

    deadline = consequence

    task = pverb <' '> role-b / verb / (verb <(' the ' / ' a ' / ' an ')> item) / (verb <' '> item)
    role-b = name

    pverb = 'kill' / 'kill'<'s'> / 'refund'<'s'> / 'refund'

    consequence =
        [<'The ' / 'the '>] character <' will '>? <' '> (move / bverb / cverb / item)
        | [<'The ' / 'the '>] item <' '> verb

    item = [<'The ' / 'the '>] word

    <whitespace> = #'\\s\\s'

    <name> = [<'The ' / 'the '>] cwords
    <words> = word (<' '> word)*
    <cwords> = cword (<' '> ['of'<' '>] cword)*
    <cword> = #'[A-Z][0-9a-zA-Z\\-\\_\\']*'
    <the> = <'The ' | 'the '>
    <word> = #'[0-9a-zA-Z\\-\\_\\']*'"
   ))


(defn parse-defs
  [text]
  (insta/add-line-and-column-info-to-metadata
   text
   (def-parser text)))

(defn parse-trope
  [text]
  (let [defs (make-defs-map (parse-defs text))
        parser (trope-parser-fn defs)]
    (insta/add-line-and-column-info-to-metadata
     (:trope defs)
     (parser (:trope defs)))
    ))

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
