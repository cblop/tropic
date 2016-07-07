(ns tropic.solver
  (:require
   [tropic.instal :refer [event-name instal-file bridge-file]]
   [clojure.java.io :as io]
   [clojure.java.shell :refer [sh]]
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
        tropenames (str "tropeBridge " (stringer (vec (set (map :label tropes)))))
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

;; (defn make-bridge [hmap id]
;;   (dorun (map #(bridge-file (assoc hmap :tropes [%]) (str "resources/" id "-" (event-name (:label %)) ".ial")) (:tropes hmap))))

(defn make-instal [hmap id]
  (dorun (map #(instal-file (assoc hmap :tropes [%]) (:tropes hmap) (str "resources/" id "-" (event-name (:label %)) ".ial")) (:tropes hmap))))

(defn make-bridge [hmap id]
  (bridge-file (:tropes hmap) (str "resources/" id "-bridge.ial")))

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
        ]
   (do
     (make-domain hmap id)
     (make-instal hmap id)
     (make-bridge hmap id)
     (make-query [] id)
     ;; (let [output (apply sh (concat ["python" "instal/instalsolve.py" "-v" "-i"] ials ["-d" (str "resources/domain-" id ".idc") "-q" (str "resources/query-" id ".iaq")]))]
     (let [output (apply sh (concat ["python2" "instal-linux/instalsolve.py" "-v" "-i"] ials ["-d" (str "resources/domain-" id ".idc") "-q" (str "resources/query-" id ".iaq")]))]
       (do
         (spit (str "resources/output-" id ".lp") output)
         ;; (clean-up id)
         {:id id
          :text "Welcome to the world of adventure!"}))
     )))

(defn event-to-text [{:keys [player verb object-a object-b]}]
  (str "observed(" verb "(" (event-name player) (if object-a (str "," object-a (if object-b (str "," object-b)) ")")) ")\n"))

(defn solve-story [id tropes event]
  (let [trps (map :label tropes)
        ials (map #(str "resources/" id "-" (event-name %) ".ial") trps)
        domain (str "resources/domain-" id ".idc")
        temp (str "resources/temp-" id ".lp")
        query (str "resources/query-" id ".iaq")
        bridge (str "resources/" id "-bridge.ial")
        outfile (str "resources/output-" id ".json")
        debug (str "resources/debug-" id ".lp")
        ]
    (do
      (spit query (event-to-text event) :append true)
      ;; (let [output (apply sh (concat ["python" "instal/instalsolve.py" "-v" "-i"] ials ["-d" domain "-q" query]))]
      (let [output (apply sh (concat ["python2" "instal-linux/instalsolve.py" "-v" "-i"] ials ["-b" bridge "-d" domain "-q" query "-j" outfile "-o" "resources/output"]))]
        (spit debug (:out output))
        (if (:out output)
          {:text (:out output)}
          {:text output})))))

