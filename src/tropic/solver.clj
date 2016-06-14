(ns tropic.solver
  (:require
   [tropic.instal :refer [event-name instal-file]]
   [clojure.java.io :as io]
   [me.raynes.conch :refer [programs with-programs let-programs] :as sh]))

(programs python clingo)

(defn random-character []
  "Random Character")

(defn random-object []
  "Random Object")

(defn random-place []
  "Random Place")

(defn stringer [item]
  (reduce str (interpose " " (map #(if (nil? %) "random" (event-name %)) item))))

(defn make-domain [hmap id]
  (let [tropes (:tropes hmap)
        p (println "TROPES:")
        p (println hmap)
        p (println (:characters hmap))
        tropenames (stringer (vec (set (map :label tropes))))
        characters (:characters hmap)
        charnames (stringer (map :label characters))
        roles (stringer (vec (set (map :role characters))))
        places (:places hmap)
        placenames (stringer (map :label places))
        locations (stringer (vec (set (map :location places))))
        objects (:objects hmap)
        objectnames (stringer (map :label objects))
        types (stringer (vec (set (map :type objects))))
        phases (reduce str (interpose " " ["inactive" "done" "phaseA" "phaseB" "phaseC" "phaseD" "phaseE" "phaseF" "phaseG" "phaseH" "phaseI" "phaseJ"]))
        strings ["Identity: id" (if (seq tropes) (str "\nTrope: " tropenames)) "\nPhase: " phases (if (seq characters) (str "\nAgent: " charnames)) (if (seq characters) (str "\nRole: " roles)) (if (seq places) (str "\nPlace: " locations)) (if (seq places) (str "\nPlaceName: " placenames)) (if (seq objects) (str "\nObject: " types)) (if (seq objects) (str "\nObjectName: " objectnames))]
        final (reduce str strings)
        ]
    (do (spit (str "resources/domain-" id ".idc") final)
        {:text final})
    ))

(defn make-instal [hmap id]
  (dorun (map #(instal-file (assoc hmap :tropes [%]) (str "resources/" id "-" (event-name (:label %)) ".ial")) (:tropes hmap))))

(defn make-query [events id]
  (spit (str "resources/query-" id ".iaq") ""))

(defn clean-up [id]
  (do
    (io/delete-file (str "resources/domain-" id ".idc"))
    (io/delete-file (str "resources/story-" id ".ial"))
    (io/delete-file (str "resources/temp-" id ".lp"))
    (io/delete-file (str "resources/query-" id ".lp"))
    (io/delete-file (str "resources/output-" id ".lp"))
    true
    ))

(defn make-story [hmap id]
  (let [trps (map :label (:tropes hmap))
        ials (map #(str "resources/" id "-" (event-name %) ".ial") trps)
        p (println (apply str (interpose " " ials)))]
   (do
     (make-domain hmap id)
     (make-instal hmap id)
     (make-query [] id)
     (let [output (python "instal/instalsolve.py" "-v" "-i" (reduce str (interpose " " ials)) "-d" (str "resources/domain-" id ".idc") "-o" (str "resources/temp-" id ".lp") (str "resources/query-" id ".iaq"))]
       (do
         (spit (str "resources/output-" id ".lp") output)
         ;; (clean-up id)
         {:id id
          :text "Welcome to the world of adventure!"}))
     )))

(defn event-to-text [{:keys [player verb object-a object-b]}]
  (str "observed(" verb "(" (event-name player) (if object-a (str "," object-a (if object-b (str "," object-b)) ")")) ")\n"))

(defn solve-story [id event]
  (let [story (str "resources/story-" id ".ial")
        domain (str "resources/domain-" id ".idc")
        temp (str "resources/temp-" id ".lp")
        query (str "resources/query-" id ".iaq")
        outfile (str "resources/output-" id ".lp")]
    (do
      (spit query (event-to-text event) :append true)
      (let [output (python "instal/instalsolve.py" "-v" "-i" story "-d" domain "-o" temp query)]
        (spit outfile output)
        {:text output}))))
