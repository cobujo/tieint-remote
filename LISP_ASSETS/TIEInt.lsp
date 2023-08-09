(defun c:WriteDimPoints (handle path / dim pt1 pt2 filename f json)
  (setq dim (handent handle))
  (if (null dim)
    (princ "\nInvalid handle.")
    (progn
      (setq dim (entget dim))
      (setq pt1 (cdr (assoc 13 dim))) ; Start point of the first extension line
      (setq pt2 (cdr (assoc 14 dim))) ; Start point of the second extension line

      ; Construct a JSON string
      (setq json (strcat "{"
                         "\"point1\": \"" (vl-princ-to-string pt1) "\","
                         "\"point2\": \"" (vl-princ-to-string pt2) "\""
                         "}"))

      ; Create the filename using the handle and the provided path
      (setq filename (strcat path "\\" handle ".json")) ; Concatenates the path and handle to form the filename
      (setq f (open filename "w"))
      
      ; Write the JSON string to the file
      (write-line json f)
      
      (close f)
    )
  )
)
