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
        cat (reduce str the)
        san (str/replace cat #"\"" "")
        lcase (str/lower-case san)]
    lcase))

(inst-event-str ["hero's" "journey"])



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

(defn get-perm
  [ptree]
  (let [char (get-char ptree)
        task (get-task ptree)]
    (hash-map :char char :task task)))

(defn get-sit-perms
  [sitdef]
  (let [rperms (html/select sitdef [:permission])]
    (map get-perm rperms)))

(defn get-obl
  [ptree]
  (let [char (get-char ptree)
        task (get-task ptree)]
    (hash-map :char char :task task)))

(defn get-sit-obls
  [sitdef]
  (let [robls (html/select sitdef [:obligation])]
    (map get-obl robls)))

(defn get-situation
  [sitdef]
  (let [header (get-sit-header sitdef)
        perms (get-sit-perms sitdef)
        obls (get-sit-obls sitdef)]
    (hash-map :situation header :perms perms :obls obls)))

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


(defn situationdef-to-instal
  "Input: {:situation {:event 'intSituationName', :params ['hero']}
                    , :obls ({:task 'doSomething', :char 'hero'})
                    , :perms ({:task 'doSomething', :char 'hero'})}"
  [sitdef]
  (let [ps (interpose "," (seq (:params (:situation sitdef))))
        sps (reduce str ps)
        header (str (:event (:situation sitdef)) "(" sps ")")
        perm-string (fn [x] (str "perm(" (:task x) "(" (:char x) "))"))
        obl-string (fn [x] (str "obl(" (:task x) "(" (:char x) "))"))
        perms (reduce str (interpose ", " (map perm-string (:perms sitdef))))
        obls (reduce str (interpose ", " (map obl-string (:obls sitdef))))
        ]
    (str header " initiates " (reduce str (interpose ", " [perms obls])) ";\n")
    )
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

