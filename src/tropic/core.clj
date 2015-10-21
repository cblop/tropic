(ns tropic.core
  (:require [instaparse.core :as insta]))

(def tropical
  (insta/parser
   "narrative = rule+
    <rule> = tropedef | situationdef | taskdef | consequencedef | storydef

    tropedef =
        tropename (<'\\nIt begins when '> event <'\\n'>) (<'Then '> event <'\\n'>)* (<'It ends when '> event <'\\n'>?)

    <tropename> =
        <'The '?> trope <' is a trope' '.'?>

    situationdef = situation <'\\n'> (permission / obligation) [(<'\\n'> (permission / obligation))* (<'\\nFinally, '> (permission / obligation) <'\\n'>?)]

    situation =
        <'When '> event

    event =
        character <' is '> <'in ' / 'at '> place
        | character <whitespace> task

    place = <'the '?> name

    character = <'The ' / 'the '>? name

    taskdef =
        taskname <'\\nTo complete it, '> item <' must be '> state <'.'?> <'\\nOtherwise, '> consequence <'.'?> <'\\n'?>
    <taskname> =
        task <' is a task' '.'?>

    consequencedef =
        consequencename <'\\n'?>
        | consequencename (<'\\nIf it happens, '> consequence) <'\\n'?>
        | consequencename (<'\\nIf it happens, '> consequence)+ <'\\nFinally, '> consequence <'\\n'?>

    <consequencename> =
        consequence <' is a consequence' '.'?>

    permission = character <' may '> task
    obligation = character <' must '> task
    task = verb | verb <(' the ' / ' a ')> item | verb <' '> item | visit
    visit = <'leave ' | 'return to ' | 'go to ' | 'visit '> place
    verb = word
    place = word

    consequence = [<'The ' / 'the '>] item <' '> verb

    item = [<'The ' / 'the '>] (word / word <' '> word)
    state = word
    storydef =
        storyname (<'\\n'> (storytrope / storyrole))+ <'\\nThe end' '.'?> <'\\n'?>
    <storyname> =
        story <' is a story' '.'?>
    <storytrope> =
        <'It contains the '> trope <' trope' '.'?>
    storyrole =
        character <' is its '> role <'.'?>

    story = [<'The ' / 'the '>] (word / word <' '> word)
    role = word
    trope = [<'The ' / 'the '>] (word / word <' '> word)
    <name> = [<'The ' / 'the '>] (word / word <' '> !'gets ' word)
    <whitespace> = #'\\s+'
    <words> = word (<whitespace> word)*
    <word> = #'[0-9a-zA-Z\\-\\_\\']*'"
))


