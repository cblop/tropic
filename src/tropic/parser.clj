(ns tropic.parser
  (:require [instaparse.core :as insta]
            [clojure.string :as str]))

(def tropical
  (insta/parser
   "narrative = rule+
    <rule> = tropedef | situationdef | taskdef | roledef | storydef | initialdef | tracedef | typedef

    tropedef =
        tropename (<'\\n' whitespace> event <'\\n'>) (<whitespace 'Then '> event <'\\n'>)* (<whitespace 'Finally, '> event <'\\n'>?)

    <tropename> =
        <'The '?> trope <' is a trope where:'>

    situation =
        <'When '> event <':'>

    situationdef = situation <'\\n'> norms+ <'\\n'?>

    roledef = rolehead power+

    typedef = <'A ' / 'An '> child <' is a type of '> parent <'.'? '\\n'?>

    <rolehead> = <('The ' / 'A ')> role <' can:\\n'>

    power = <whitespace> verb <' the '?> character <'\\n'?>

    role = word | word <' '> word
    parent = word | word <' '> word
    child = word | word <' '> word

    initialdef = <'Initially:'> (<'\\n'> <whitespace> (event / norms))+ <'\\n'?>

    tracedef = <'In story '> label <':'> (<'\\n'> <whitespace> event)+

    label = word

    norms = permission | obligation

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

    permission = <whitespace> character <' may '> task conditional?
    obligation = <whitespace> character <' must '> task <' before '> deadline <'\\n' whitespace 'Otherwise, '> <'the '?> violation <'.'?> <'\\n'?>

    violation = event

    deadline = consequence

    task = verb | verb <(' the ' / ' a ')> item | verb <' '> item | visit
    visit = ('leave' <' '>) | ('return' (<' '> 'to')? <' '>) | ('go' / 'goes') (<' '> 'to')? <' '> | ('visit' <' '>) place
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
    <whitespace> = #'\\s\\s+'
    <words> = word (<whitespace> word)*
    <word> = #'[0-9a-zA-Z\\-\\_\\']*'"
   ;; :output-format :enlive
))

(defn parse
  [text]
  (insta/add-line-and-column-info-to-metadata
   text
   (tropical text)))


(defn strip-name
  "Takes character name list, strips off 'the', makes lowercase"
  [n]
  (let [the (remove #(or (= "the" %) (= "The" %)) n)
        ;; camel (if (> (count the) 1)
                ;; (cons (str/lower-case (first the)) (map str/capitalize (rest the)))
                ;; (map str/lower-case the))
        camel (map str/capitalize the)
        cat (reduce str camel)
        san (str/replace cat #"\"" "")
        ]
    san))

(defn event-str
  "Takes list of strings, converts to exampleEvent format"
  [{:keys [params name]}]
  (let [sanstrings (map #(str/replace % #"'" "") name)
        sparams (reduce str (interpose ", " params))
        svec (cons (str/lower-case (first sanstrings)) (map str/capitalize (rest sanstrings)))
        pstr (str "(" sparams ")")
        outvec (conj (vec svec) pstr)
        ]
    ;; (with-meta (symbol (reduce str outvec)) {:params params})
    (reduce str outvec)
    ))

(defn inst-str
  [sym]
  (let [s (str sym)
        caps (apply str (str/upper-case (first s)) (rest s))]
    (str "int" caps)))

(defn vio-str
  [sym]
  (let [s (str sym)
        caps (apply str (str/upper-case (first s)) (rest s))]
    (str "vio" caps)))

(defn inst-event-str
  "Takes list of strings, converts to intExampleEvent format"
  [argm]
  (let [estr (event-str argm)]
    (inst-str estr)
    ))

(defn inst-tree
  [x xs]
  (inst-event-str {:params [x] :name xs}))


(defn m
  [old new]
  (with-meta new (meta old)))

(defn event-tree
  [x xs]
  (m xs (symbol (event-str {:params [x] :name xs}))))

(defn get-line
  [obj]
  (- (:instaparse.gll/start-line (meta obj)) 1))

(defn get-comment
  [text data]
  (let [line (get-line data)]
    (str "; % " (nth (str/split-lines text) line) "\n")))

(defn get-next-comment
  [text data]
  (let [line (+ (get-line data) 1)]
    (str "; % " (nth (str/split-lines text) line) "\n")))

(defn get-prev-comment
  [text data]
  (let [line (- (get-line data) 1)]
    (str "; % " (nth (str/split-lines text) line) "\n")))

(defn perm-tree
  [x xs]
  (let [args (event-tree x xs)]
    (str "perm(" args ")")))

(defn obl-tree
  [char task deadline consequence]
  (let [args (event-tree char task)
        vio (vio-str args)
        body (str "obl(" args ", " deadline ", " vio ")")
        ]
    body
    ))

(defn vio-tree
  [char task deadline consequence]
  (let [args (event-tree char task)
        vio (vio-str args)
        vio-event (str vio " generates " consequence)]
    vio-event))

(defn tropedef-tree
  [text name & args]
  (let [evs (map inst-str args)
        comments (map #(get-comment text %) args)
        firstcomment (str/replace (get-comment text name) "; " "")
        firstline (str name " generates " (first evs) (first comments))
        gens (map #(interpose " generates " %) (partition 2 1 evs))
        cgens (map (fn [x y] (conj (vec x) y)) gens (rest comments))
        genstr (apply str (flatten cgens))
        ]
    (with-meta (symbol (str firstcomment firstline genstr)) {:type "trope" :events evs})
    ))

(defn sitdef-tree
  [text name & args]
  (let [comment (str/replace (get-comment text name) "; " "")
        genstr (map #(str (first name) " initiates " %) args)]
    (with-meta (symbol (str comment (reduce str genstr))) {:type "situation"})
    ))

(defn add-comment
  [line]
  (str "  %" (meta line) "\n" line)
  )

(defn statements [strings]
  (reduce str (interpose "\n" strings)))

(defn typedef-tree
  [text & args]
  (let [
        ;; parent (first (filter #(= "parent" (:type (meta %)))))
        child (first (filter #(= "child" (:type (meta %))) args))
        comment (get-comment text child)]
    (with-meta (symbol (str child comment)) {:type "type"})))

(defn narrative-tree
  [& args]
  (let [type-header "%% TYPES ---------------------\n"
        instev-header "%% INST EVENTS ------------------------\n"
        trope-header "%% TROPES ---------------------\n"
        scene-header "%% SCENES ---------------------\n"
        tropes (filter #(= (:type (meta %)) "trope") args)
        trope-strs (statements tropes)

        ;; Base types: Character, Object
        types (concat ["Character;\n" "Object;\n"] (filter #(= (:type (meta %)) "type") args))
        typedecs (reduce str (map #(str "type " %) types))

        instdecs (reduce str (map #(str "inst event " % ";\n") (mapcat #(flatten (:events (meta %))) tropes)))
        situations (filter #(= (:type (meta %)) "situation") args)
        sit-strs (statements situations)
        ]
    ;; (reduce str (interpose "\n" outs))
    (str type-header typedecs "\n"
         instev-header instdecs "\n"
         trope-header trope-strs "\n"
         scene-header sit-strs)
    ))


(defn obl-text
  [text args]
  (str (apply obl-tree args) (get-comment text (second args)) (apply vio-tree args) (get-next-comment text (second args))))


(defn transform
  [ptree text]
  (insta/transform
   {
    :trope (fn [& args] (m (first args) (symbol (inst-event-str {:name args}))))
    :verb (fn [& args] args)
    :item (fn [& args] args)
    :character (fn [& args] (strip-name args))
    :task (partial concat)
    :event event-tree
    :consequence (fn [s v] (event-str {:params [(strip-name s)] :name v}))
    :violation str
    :deadline str
    :norms str
    :situation (fn [& args] args)
    :permission (fn [& args] (str (apply perm-tree args) (get-comment text (second args))))
    :obligation (fn [& args] (obl-text text args))
    :tropedef (partial tropedef-tree text)
    :situationdef (partial sitdef-tree text)
    :child (fn [& args] (with-meta (symbol (strip-name args)) {:type "child"}))
    :parent (fn [& args] (with-meta (symbol (strip-name args)) {:type "parent"}))
    :typedef (partial typedef-tree text)
    :narrative narrative-tree
    } ptree))

