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

    situationdef = situation <'\\n'> norms [(<'\\n'> norms)* (<'\\nFinally, '> norms <'\\n'>?)]

    norms = permission | obligation

    situation =
        <'When '> event

    conditional =
        <' if '> <'they '?> event

    event =
        character <' '> task

    place = name

    character = name

    taskdef =
        taskname condition <'\\nOtherwise, '> <'the '?> event <'.'?> <'\\n'?>

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

    permission = character <' may '> task conditional?
    obligation = character <' must '> task <' before '> deadline <'\\nOtherwise, '> <'the '?> violation <'.'?> <'\\n'?>
    violation = event
    deadline = consequence
    task = verb | verb <(' the ' / ' a ')> item | verb <' '> item | visit
    visit = ('leave' <' '>) | ('return' (<' '> 'to')? <' '>) | 'go' (<' '> 'to')? <' '> | ('visit' <' '>) place
    verb = word
    place = word

    consequence =
        [<'The ' / 'the '>] item <' '> verb
        | [<'The ' / 'the '>] character <' will '> task

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

(defn event-str
  "Takes list of strings, converts to exampleEvent format"
  [strings]
  (let [sanstrings (map #(str/replace % #"'" "") strings)
        fstr (first (map str/lower-case sanstrings))
        ;; fstr (first sanstrings)
        svec (cons fstr (map str/capitalize (rest sanstrings)))
        ]
    (reduce str svec)))

(defn inst-event-str
  "Takes list of strings, converts to intExampleEvent format"
  [strings]
  (let [sanstrings (map #(str/replace % #"'" "") strings)
        svec (concat ["int"] (map str/capitalize sanstrings))]
      (reduce str svec)))

(defn task-str
  "Takes list of strings, converts to (doThing) format"
  [strings]
  (let [sanstrings (map #(str/replace % #"'" "") strings)
        svec (cons (str/lower-case (first sanstrings)) (map str/capitalize (rest sanstrings)))]
    (reduce str svec)))

(defn strip-name
  "Takes character name list, strips off 'the', makes lowercase"
  [n]
  (let [the (remove #(or (= "the" %) (= "The" %)) n)
        camel (if (> (count the) 1) (cons (str/lower-case (first the)) (map str/capitalize (rest the))) the)
        cat (reduce str camel)
        san (str/replace cat #"\"" "")
        ]
    san))

(defn get-sit-header
  [sitdef]
  (let [revent (first (html/select sitdef [:situation :event]))
        rchar (:content (first (html/select revent [:character])))
        char (strip-name rchar)
        ritem (map :content (html/select sitdef [:event :item]))
        rverb (map :content (html/select sitdef [:event :verb]))
        revent (map concat rverb ritem)
        event (first (map inst-event-str revent))
        emap (hash-map :params [char] :event event) ;;change this
        ]
    emap
    ))

(defn get-char
  [ptree]
  (strip-name (:content (first (html/select ptree [:character])))))

(defn get-event
  [ptree]
  (let [item (map :content (html/select ptree [:event :item]))
        verb (map :content (html/select ptree [:event :verb]))
        revent (map concat verb item)]
    (first (map inst-event-str revent))))

(defn get-task
  [ptree]
  (let [item (map :content (html/select ptree [:task :item]))
        verb (map :content (html/select ptree [:task :verb]))
        place (first (map :content (html/select ptree [:task :visit :place])))
        revent (map concat verb item)]
    (if (empty? place)
      (first (map task-str revent))
      (str "visit" (str/capitalize (task-str place)))
      )))

(defn get-cond
  [ptree]
  (let [cond (first (map :content (html/select ptree [:conditional])))
        item (map :content (html/select cond [:event :item]))
        verb (map :content (html/select cond [:event :verb]))
        char (map :content (html/select cond [:character]))
        revent (first (map concat verb item))
        event (event-str revent)
        cond-str (str event (strip-name char))
        ]
    cond-str))

(defn get-perm
  [ptree]
  (let [char (get-char ptree)
        task (get-task ptree)
        cond (get-cond ptree)]
    (if (or (empty? cond) (nil? cond))
      (hash-map :char char :task task)
      (hash-map :char char :task task :cond cond))))

(defn get-sit-perms
  [sitdef]
  (let [rperms (html/select sitdef [:norms :permission])]
    (map get-perm rperms)))

(defn get-deadline
  [ptree]
  (let [verb (first (map :content (html/select ptree [:deadline :verb])))
        item (first (map :content (html/select ptree [:deadline :item])))
        event (str (event-str verb) "(" (event-str item) ")")
        ]
    event))

(defn get-consequence
  [ptree]
  (let [
        verb (first (map :content (html/select ptree [:violation :verb])))
        item (first (map :content (html/select ptree [:violation :item])))
        char (first (map :content (html/select ptree [:violation :character])))
        event (str (event-str verb) "(" (strip-name char) ", " (event-str item) ")")
        ]
    event))

(defn get-obl
  [ptree]
  (let [char (get-char ptree)
        task (get-task ptree)
        deadline (get-deadline ptree)
        consequence (get-consequence ptree)]
    {:char char
     :task task
     :deadline deadline
     :consequence consequence}))

(defn get-sit-obls
  [sitdef]
  (let [robls (html/select sitdef [:norms :obligation])]
    (map get-obl robls)))

(defn get-situation
  [sitdef]
  (let [header (get-sit-header sitdef)
        perms (get-sit-perms sitdef)
        obls (get-sit-obls sitdef)]
    (hash-map :situation header :perms perms :obls obls)))

(defn get-situations
  [ptree]
  (map get-situation (html/select ptree [:situationdef])))

(defn get-task-condition
  [ptree]
  (let [item (first (map :content (html/select ptree [:condition :item])))
        state (first (map :content (html/select ptree [:condition :state])))
        item-str (task-str item)
        state-str (task-str state)
        ]
    (str state-str "(" item-str ")")))

(defn get-task-consequence
  [ptree]
  (let [character (first (map :content (html/select ptree [:event :character])))
        verb (first (map :content (html/select ptree [:event :verb])))
        item (first (map :content (html/select ptree [:event :item])))
        char (strip-name character)
        ]
    {:character char
     :task (str (task-str verb) "(" (task-str item) ")")}))


(defn get-taskdef
  [taskdef]
  (let [task (get-task taskdef)
        condition (get-task-condition taskdef)
        consequence (get-task-consequence taskdef)]
    {:task task
     :condition condition
     :consequence consequence}))

(defn get-tropes
  [ptree]
  (map get-trope (html/select ptree [:tropedef])))

(defn get-trope
  "Input: tropedef part of the parsetree
  Output: {:name 'intTropeName', :params #{'param'},
            :events ({:event 'event1' :char 'char1'}
                     {:event 'event2' :char 'char2'})}"
  [tropedef]
  (let [rname (:content (first (html/select tropedef [:trope])))
        name (inst-event-str rname)
        rchar (map :content (html/select tropedef [:event :character]))
        chars (map strip-name rchar)
        ritem (map :content (html/select tropedef [:event :item]))
        rverb (map :content (html/select tropedef [:event :verb]))
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

(defn compile-instal
  [ptree]
  (let [tcomment "%% TROPES ---------------------\n"
        tropes (reduce str (map tropedef-to-instal (get-tropes ptree)))
        scomment "%% SCENES ---------------------\n"
        sits (reduce str (map situationdef-to-instal (get-situations ptree)))]
    (str tcomment tropes "\n" scomment sits)))


(defn perm-string
  [p]
  (let [cond (if (or (empty? (:cond p)) (nil? (:cond p))) "" (str " if " (:cond p)))]
    (str "perm(" (:task p) "(" (:char p) "))" cond)))

(defn obl-string
  [o]
  (let [viol (str "vio" (str/capitalize (:task o)) "(" (:char o) ")")
        vevent (str viol " generates " (:consequence o))]
    (str "obl(" (:task o) "(" (:char o) "), " (:deadline o) ", " viol ");\n" vevent)))

(defn init-string
  [n]
  (str "initiates " n ";\n"))


(defn taskdef-to-instal
  [])

(defn situationdef-to-instal
  "Input: {:situation {:event 'intSituationName', :params ['hero']}
                    , :obls ({:task 'doSomething', :char 'hero' :cond 'hasSomething(hero)'})
                    , :perms ({:task 'doSomething', :char 'hero'})}
  (conds are optional)"
  [sitdef]
  (let [ps (interpose "," (seq (:params (:situation sitdef))))
        sps (reduce str ps)
        header (str (:event (:situation sitdef)) "(" sps ") ")
        perms (reduce str (map #(str header (init-string %)) (map perm-string (:perms sitdef))))
        obls (reduce str (map #(str header (init-string %)) (map obl-string (:obls sitdef))))
        ]
    (str perms obls)
    )
  )

