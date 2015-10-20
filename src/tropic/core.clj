(ns tropic.core
  (:require [instaparse.core :as insta]))

(def tropical
  (insta/parser
   "narrative = rule+
    rule = tropedef | situationdef | taskdef | storydef
    <tropedef> =
        tropename (<'\\nIt begins when '> event <'\\n'>) (<'Then '> event <'\\n'>)* (<'It ends when '> event <'\\n'>?)
    <tropename> =
        <'The '?> trope <' is a trope' '.'?>
    <situationdef> = situation <'\\n'> (permission / obligation) [(<'\\n'> (permission / obligation))* (<'\\nFinally, '> (permission / obligation) <'\\n'>?)]
    situation =
        <'When '> event
    event =
        character <' is '> <'in ' / 'at '> place
        | character <' gets '> <'a ' / 'an '> task
        | character <whitespace> task
    place = <'the '?> name
    character = <'The ' / 'the '>? name
    taskdef =
        taskname <'\\nTo complete it, '> item <' must be '> state <'.'?> <'\\nOtherwise, '> consequence <'.'?> <'\\n'?>
    taskname =
        task <' is a task' '.'?>
    permission = character <' may '> task
    obligation = character <' must '> task
    task = verb | verb <(' the ' / ' a ')> item | visit
    visit = <'leave ' | 'return to ' | 'go to ' | 'visit '> place
    verb = word
    place = word
    consequence = item <' '> verb
    item = [<'The ' / 'the '>] (word / word <' '> word)
    state = word
    <storydef> =
        storyname
    <storyname> =
        story <' is a story' '.'?>
    story = word
    trope = words
    <name> = word
    <whitespace> = #'\\s+'
    <words> = word (<whitespace> word)*
    <word> = #'[0-9a-zA-Z\\-\\_\\']*'"
))


