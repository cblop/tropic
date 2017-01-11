(ns tropic.solver
  (:require
   [tropic.instal :refer [event-name instal-file bridge-file]]
   [clojure.java.io :as io]
   [tropic.gen :refer [make-map make-inst-map]]
   [tropic.parser :refer [parse-trope parse-char parse-object parse-place]]
   [tropic.text-parser :refer [query-parse answer-set-to-map]]
   [clojure.java.shell :refer [sh]]
   [me.raynes.conch :refer [programs with-programs let-programs] :as sh]))

(programs python2 clingo)

(def ARCH (if (= (System/getProperty "os.name") "Mac OS X") "instal"
               (if (= (System/getProperty "os.arch") "amd64") "instal-linux" "instal-arm")))

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
    (do (spit (str "resources/" id "/domain-" id ".idc") final)
        {:text final})
    ))

;; (defn make-bridge [hmap id]
;;   (dorun (map #(bridge-file (assoc hmap :tropes [%]) (str "resources/" id "-" (event-name (:label %)) ".ial")) (:tropes hmap))))

(defn make-instal [hmap id]
  (dorun (map #(instal-file (assoc hmap :tropes [%]) (:tropes hmap) (str "resources/" id "/" id "-" (event-name (:label %)) ".ial")) (:tropes hmap))))

(defn make-bridge [hmap id]
  (bridge-file (:tropes hmap) (str "resources/" id "/" id "-bridge.ial")))

(defn make-query [events id]
  (spit (str "resources/" id "/query-" id ".iaq") ""))

(defn clean-up [id]
  (do
    (io/delete-file (str "resources/domain-" id ".idc"))
    (io/delete-file (str "resources/story-" id ".ial"))
    (io/delete-file (str "resources/temp-" id ".lp"))
    (io/delete-file (str "resources/query-" id ".lp"))
    (io/delete-file (str "resources/output-" id ".lp"))
    true
    ))


(defn clean-up-traces [id]
  (let [dir (io/file (str "resources/" id))
        files (file-seq dir)]
    (doseq [f file-seq] (io/delete-file f))))


(defn make-story [hmap id]
  (let [trps (map :label (:tropes hmap))
        ials (map #(str "resources/" id "/" id "-" (event-name %) ".ial") trps)
        debug (str "resources/" id "/debug-" id ".lp")
        constraint "resources/constraint.lp"
        ]
   (do
     (.mkdir (java.io.File. (str "resources/" id)))
     (.mkdir (java.io.File. (str "resources/" id "/traces")))
     (make-domain hmap id)
     (make-instal hmap id)
     (make-bridge hmap id)
     (make-query [] id)
     ;; (let [output (apply sh (concat ["python2" "instal/instalsolve.py" "-v" "-i"] ials ["-d" (str "resources/domain-" id ".idc") "-q" (str "resources/query-" id ".iaq")]))]
     ;; (let [output (apply sh (concat ["python2" "instal-linux/instalquery.py" "-v" "-i"] (conj ials (str "resources/" id "/constraint.lp")) ["-l 1" "-n 0" "-x" (str "resources/" id "traces/trace-" id "-.lp")  "-d" (str "resources/" id "/domain-" id ".idc")]))]
     (let [output (apply sh (concat ["python2" (str ARCH "/instalquery.py") "-v" "-i"] (conj ials constraint) (if (> (count ials) 1) ["-b" (str "resources/" id "/" id "-bridge.ial")]) ["-l 1" "-n 0" "-x" (str "resources/" id "/traces/trace-" id "-.lp") "-d" (str "resources/" id "/domain-" id ".idc")]))
           tracedir (clojure.java.io/file (str "resources/" id "/traces"))
           traces (filter #(.isFile %) (file-seq tracedir))
           sets (for [t traces]
                  (answer-set-to-map (slurp t)))
           ]
       (do
         (spit debug output)
         (spit (str "resources/" id "/output-" id ".lp") output)
         ;; (clean-up id)
         {:id id
          :sets sets
          :text "Welcome to the world of adventure!"}))
     )))

(defn event-to-text [{:keys [player verb object-a object-b]}]
  (str "observed(" verb "(" (event-name player) (if object-a (str "," object-a (if object-b (str "," object-b)) ")")) ")"))

(defn events-to-text[events]
  (apply str (interpose "\n" (map event-to-text events))))

(defn delete-traces [id]
  (let [tracedir (clojure.java.io/file (str "resources/" id "/traces"))
        traces (filter #(.isFile %) (file-seq tracedir))]
    (do
      (doseq [t traces]
        (io/delete-file t))
      true)))

(defn solve-story [id tropes events]
  (let [trps (map :label tropes)
        ials (map #(str "resources/" id "/" id "-" (event-name %) ".ial") trps)
        domain (str "resources/" id "/domain-" id ".idc")
        temp (str "resources/" id "/temp-" id ".lp")
        query (str "resources/" id "/query-" id ".iaq")
        bridge (str "resources/" id "/" id "-bridge.ial")
        outfile (str "resources/" id "/output-" id ".json")
        debug (str "resources/" id "/debug-" id ".lp")
        constraint "resources/constraint.lp"
        ]
    (do
      (delete-traces id)
      (spit query (events-to-text events) :append false)
      ;; (let [output (apply sh (concat ["python2" "instal/instalsolve.py" "-v" "-i"] ials ["-d" domain "-q" query]))]
      ;; (let [output (apply sh (concat ["python2" "instal-linux/instalquery.py" "-v" "-i"] (conj ials (str "resources/" id "/constraint.lp")) ["-l 1" "-n 0" "-x" (str "resources/" id "/traces/trace-" id "-.lp") "-b" bridge "-d" domain] (if events ["-q" query])))]
      (let [output (apply sh (concat ["python2" (str ARCH "/instalquery.py") "-v" "-i"] ials (if (> (count ials) 1) ["-b" bridge]) ["-l 1" "-n 0" "-x" (str "resources/" id "/traces/trace-" id "-.lp") "-d" domain] (if events ["-q" query])))
            tracedir (clojure.java.io/file (str "resources/" id "/traces"))
            traces (filter #(.isFile %) (file-seq tracedir))
            sets (for [t traces]
                   (answer-set-to-map (slurp t)))]
        (do
          (spit debug output)
          (spit outfile (:out output))
          (if (:out output)
            {:sets sets
             :text (:out output)}
            {:text output}))))))

(defn trope-map [trope]
  (let [parsed (make-map (parse-trope trope))]
    {:label (:label (:trope parsed))
     :events (:events (:trope parsed))
     :situations []})
  ;; also need: chars, obj, places?
  )

(defn st-map [name tropes chars objs places player]
  (let [trps (map trope-map tropes)
        role-pairs (map #(hash-map :class (:role %) :iname (:label %)) chars)
        obj-pairs (map #(hash-map :class (:type %) :iname (:label %)) objs)
        place-pairs (map #(hash-map :class (:location %) :iname (:label %)) places)
        story {:storyname name
               :tropes (map :label trps)
               :instances (concat role-pairs obj-pairs place-pairs)}
        ]
    {:story story
     :tropes trps
     :characters chars
     :objects objs
     :places places
     :player player
     }))

(defn make-cmd [t-files c-file o-file p-file oname player]
  (let [strs (map slurp t-files)
        c-strs (clojure.string/split-lines (slurp c-file))
        o-strs (clojure.string/split-lines (slurp o-file))
        p-strs (clojure.string/split-lines (slurp p-file))
        chars (map #(make-inst-map (parse-char %)) c-strs)
        objs (map #(make-inst-map (parse-object %)) o-strs)
        places (map #(make-inst-map (parse-place %)) p-strs)
        story-map (st-map oname strs chars objs places player)]
    (do
      (println "STORY:")
      (println story-map)
      (make-story story-map oname)
      (println "SUCCESS!")
      (println (str "Instal files are in the \"resources/" oname "\" directory.")))
    ))

