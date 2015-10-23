(ns tropic.core
  (:require [instaparse.core :as insta]
            [net.cgrand.enlive-html :as html]
            [clojure.string :as str]))

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
        character <' '> task

    place = name

    character = name

    taskdef =
        taskname condition <'\\nOtherwise, '> consequence <'.'?> <'\\n'?>

    condition =
        <'\\nTo complete it, '> item <' must be '> state <'.'?>

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
    <name> = (<'The ' | 'the '>)? word | (word <' '> !'gets ' word)
    <whitespace> = #'\\s+'
    <words> = word (<whitespace> word)*
    <word> = #'[0-9a-zA-Z\\-\\_\\']*'"
   :output-format :enlive
))

(defn inst-event-str
  "Takes list of strings, converts to intExampleEvent format"
  [strings]
  (let [sanstrings (map #(str/replace % #"'" "") strings)
        svec (concat ["int"] (map str/capitalize sanstrings))]
      (reduce str svec)))

(defn strip-name
  "Takes character name list, strips off 'the', makes lowercase"
  [n]
  (let [the (remove #(or (= "the" %) (= "The" %)) n)
        cat (reduce str the)
        san (str/replace cat #"\"" "")
        lcase (str/lower-case san)]
    lcase))

(inst-event-str ["hero's" "journey"])

(defn get-situation
  [ptree]
  (let [sits (html/select ptree [:narrative :situationdef])
        ]
    ))

(defn get-trope
  "Output: {:name 'intTropeName', :params #{'param'},
            :events ({:event 'event1' :char 'char1'}
                     {:event 'event2' :char 'char2'})}"
  [ptree]
  (let [;;tropes (html/select ptree [:narrative :tropedef])
        rname (:content (first (html/select ptree [:narrative :tropedef :trope])))
        name (inst-event-str rname)
        rchar (map :content (html/select ptree [:narrative :tropedef :event :character]))
        chars (map strip-name rchar)
        ritem (map :content (html/select ptree [:narrative :tropedef :event :item]))
        rverb (map :content (html/select ptree [:narrative :tropedef :event :verb]))
        revents (map concat rverb ritem)
        events (map inst-event-str revents)
        emap (map #(hash-map :char %1 :event %2) chars events)
        tmap {:name name
              :params (set chars)
              :events emap}
        ]
    tmap
    ))

(defn tropedef-to-instal
  "Input: {:name 'intTropeName', :params #{'param'},
           :events ({:event 'event1' :char 'char1'}
                    {:event 'event2' :char 'char2'})}"
  [tropedef]
  (let [ps (interpose "," (seq (:params tropedef)))
        sps (reduce str ps)
        string-params (fn [x] (str (:event x) "(" (:char x) ")"))
        root (str (:name tropedef) "(" sps ")")
        events (map string-params (:events tropedef))
        firstline (str root " generates " (first events))
        gens (map #(interpose " generates " %) (partition 2 1 events))
        genstr (apply str (flatten (interpose ";\n" gens)))
        ]
    (str firstline ";\n" genstr ";\n")
  ))


(defn situationdef-to-instal
  [sitdef]
  )


(defn instal
  [parsetree]
  (let [tropdef {:name }]))

(defn instal
  [parsetree]
  (insta/transform {:trope (fn [& args] (inst-event-str args) )
                    :event (fn [char task]
                             (let [name (strip-name (rest char))
                                   v (rest (second task))
                                   i (rest (nth task 2))
                                   ]
                               (str (inst-event-str (concat v i)) "(" name ")")
                               ))
                    } parsetree))

