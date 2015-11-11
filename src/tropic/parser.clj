(ns tropic.parser
  (:require [instaparse.core :as insta]
            [clojure.string :as str]))

(def tropical
  (insta/parser
   "narrative = rule+
    <rule> = tropedef | situationdef | taskdef | roledef | storydef | initialdef | tracedef

    tropedef =
        tropename <'\\n'> (alias / <whitespace> norms / sequence / <whitespace> situationdef)+ <'\\n'?>

    <tropename> =
        <'The '? '\\\"'> trope <'\\\" ' 'is a trope where:'>

    alias =
        <whitespace> character <' is also '> character <'\\n'?>

    situation =
        <'When '> event <':'>

    sequence =
        <whitespace> event or? <'\\n'?> (<whitespace> <'Then '> event or? <'\\n'?>)*

    situationdef = situation (<'\\n'> <whitespace+> norms | <'\\n'> <whitespace+> consequence)+ <'\\n'?>

    or =
        <'\\n' whitespace+ 'Or '> event

    roledef = rolehead power+

    <rolehead> = <'A ' / 'An '> role <' is a type of character who:\\n'> power*

    power = <whitespace> (can / cannot) <'\\n'?>

    can = <'Can '> verb <' '> item
    cannot = <'Cannot '> verb <' '> item

    goal = character <' wants '> (item / character) <' to '> verb

    role = word | word <' '> word

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
        taskname condition <'\\n' whitespace+ 'Otherwise, '> <'the '?> event <'.'?> <'\\n'?>

    condition =
        <'\\n' whitespace 'To complete it, '> item <' must be '> state <'.'?>

    <taskname> =
        task <' is a task' '.'?>

    permission = character <' may '> task conditional? <'\\n'?>
    obligation = character <' must '> task <' before '> deadline <'\\n' whitespace+ 'Otherwise, '> <'the '?> violation <'.'?> <'\\n'?>

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
    <whitespace> = #'\\s\\s'
    <words> = word (<whitespace> word)*
    <word> = #'[0-9a-zA-Z\\-\\_\\']*'"
   ;; :output-format :enlive
))

(def param-names ["X" "Y" "Z" "W"])

(defn parse
  [text]
  (insta/add-line-and-column-info-to-metadata
   text
   (tropical text)))

(defn strip-name
  "Takes character name list, strips off 'the', makes lowercase"
  [n]
  (let [the (remove #(or (= "the" %) (= "The" %)) n)
        camel (if (> (count the) 1)
                (cons (str/lower-case (first the)) (map str/capitalize (rest the)))
                (map str/lower-case the))
        ;; camel (map str/capitalize the)
        cat (reduce str camel)
        san (str/replace cat #"\"" "")
        ]
    san))

(defn event-str
  "Takes list of strings, converts to exampleEvent format"
  [{:keys [params name]} ls]
  (let [sanstrings (map #(str/replace % #"'" "") name)
        letters (take (count params) ls)
        ;; pmap (zipmap (map keyword letters) params)
        pmap params
        sparams (reduce str (interpose ", " letters))
        svec (cons (str/lower-case (first sanstrings)) (map str/capitalize (rest sanstrings)))
        pstr (str "(" sparams ")")
        outvec (conj (vec svec) pstr)
        ]
    ;; (with-meta (symbol (reduce str outvec)) {:params params})
    (with-meta (symbol (reduce str outvec)) {:params pmap})
    ;; "Heeey"
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
  [argm letters]
  (let [estr (event-str argm letters)]
    (inst-str estr)
    ))

(defn inst-tree
  [x xs]
  (inst-event-str {:params [x] :name xs} param-names))


(defn m
  [old new]
  (with-meta new (meta old)))

(defn event-tree
  [x xs]
  ;; (let [ev (event-str {:params [x] :name xs})]
    ;; (with-meta ev (merge (meta xs) (meta ev)))))
    (with-meta {:params [x] :name xs} (meta xs)))
  ;; (m xs (symbol (event-str {:params [x] :name xs}))))

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
  (let [args (event-tree x xs)
        pstrs (event-str args param-names)]
    (str "perm(" pstrs ")")))

(defn lookup-vars
  [vars args]
  (event-str args (map #(get vars %) (:params args))))

(defn zip-params [args]
  (let [params (map :params args)
        unique (set (flatten params))
        pzip (zipmap unique param-names)]
    pzip))

(defn if-line [pzip]
  (let [roles (map #(str "role(" (val %) ", " (key %) ")") pzip)]
    (reduce str (cons " if " (interpose ", " roles)))))

(defn obl-tree
  [char task deadline consequence]
  (let [args (event-tree char task)
        estr (event-str args param-names)
        dline (assoc deadline :params (map strip-name (:params deadline)))
        pzip (zip-params [args dline])
        vio (vio-str (lookup-vars pzip args))
        arg-params (lookup-vars pzip args)
        dead-params (lookup-vars pzip dline)
        body (str "obl(" arg-params ", " dead-params ", " vio ")")
        ifline (if-line pzip)
        ]
    (str body ifline)
    ))


(defn vio-tree
  [char task deadline consequence]
  (let [args (event-tree char task)
        pzip (zip-params [args consequence])
        vio (vio-str (lookup-vars pzip args))
        ;; x (println (type consequence) )
        vio-event (str vio " generates " (lookup-vars pzip consequence))
        ifline (if-line pzip)]
    (str vio-event ifline)))

(defn tropedef-tree
  [text name & args]
  (let [evs (map #(inst-str (event-str % param-names)) args)
        comments (map #(get-comment text %) args)
        firstcomment (str/replace (get-comment text name) "; " "")
        ;; ps (:params (meta (first args)))
        ps (map :params args)
        pstrs (map #(reduce str (map (fn [x y] (str x ", " y)) ["X" "Y" "Z" "W"] %)) ps)
        iflines (map #(str " if role(" % ")") pstrs)
        firstline (str name " generates " (first evs) (first iflines) (first comments))
        gens (map #(interpose " generates " %) (partition 2 1 evs))
        rgens (map (fn [x y] (conj (vec x) y)) gens (rest iflines))
        cgens (map (fn [x y] (conj (vec x) y)) rgens (rest comments))
        genstr (apply str (flatten cgens))
        ]
    (with-meta (symbol (str firstcomment firstline genstr)) {:type "trope" :events evs})
    ))

(defn sitdef-tree
  [text name & args]
  (let [comment (str/replace (get-comment text name) "; " "")
        genstr (map #(str (inst-event-str (first name) param-names) " initiates " %) args)]
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
        fluent-header "%% FLUENTS ---------------------\n"
        instev-header "%% INST EVENTS ------------------------\n"
        trope-header "%% TROPES ---------------------\n"
        scene-header "%% SCENES ---------------------\n"
        tropes (filter #(= (:type (meta %)) "trope") args)
        trope-strs (statements tropes)

        ;; Base types: Agent, Role, Object
        ;; types (concat ["Character;\n" "Object;\n"] (filter #(= (:type (meta %)) "type") args))
        types ["Agent" "Role" "Object"]
        typedecs (reduce str (map #(str "type " % ";\n") types))

        fluents ["role(Agent, Role)"]
        fluentdecs (reduce str (map #(str "fluent " % ";\n") fluents))

        instdecs (reduce str (map #(str "inst event " % ";\n") (mapcat #(flatten (:events (meta %))) tropes)))
        situations (filter #(= (:type (meta %)) "situation") args)
        sit-strs (statements situations)
        ]
    ;; (reduce str (interpose "\n" outs))
    (str type-header typedecs "\n"
         fluent-header fluentdecs "\n"
         instev-header instdecs "\n"
         trope-header trope-strs "\n"
         scene-header sit-strs)
    ))


(defn obl-text
  [text args]
  (str (apply obl-tree args) (get-comment text (second args)) (apply vio-tree args) (get-next-comment text (second args))))

(defn strip-the [args]
  (vec (remove #(or (= "the" %) (= "The" %)) args)))


(defn transform
  [ptree text]
  (insta/transform
   {
    :trope (fn [& args] (m (first args) (symbol (inst-event-str {:name args} param-names))))
    :verb (fn [& args] args)
    ;; :item (fn [& args] (if (> (count args) 1) (strip-the args) args))
    :item (fn [& args] args)
    :character (fn [& args] (strip-name args))
    :task (partial concat)
    :event event-tree
    ;; :consequence (fn [s v] (event-str {:params [(strip-name s)] :name v} param-names))
    :consequence event-tree
    :violation (fn [& args] (first args))
    :deadline (fn [& args] (first args))
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

