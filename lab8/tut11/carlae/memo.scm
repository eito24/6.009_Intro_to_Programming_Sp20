(begin
  ; little "dictionary" representation, as a list of cons cells
  ; makes use of set-car! and set-cdr! built-ins (not included in the writeup)
  ; for mutating cons cells
  ; unlike Python's dictionaries, looking up and setting values take time linear
  ; in the size of the dictionary, rather than constant
  (define (make-dict) (list (cons nil nil)))

  (define (dict-get dict key)
    (if (=? (car (car dict)) key)
      (cdr (car dict))
      (if (=? (cdr dict) nil)
        nil
        (dict-get (cdr dict) key)
      )
    )
  )

  (define (dict-set dict key val)
    (if (=? (car (car dict)) key)
      (set-cdr! (car dict) val)
      (if (=? (cdr dict) nil)
        (set-cdr! dict (list (cons key val)))
        (dict-set (cdr dict) key val)
      )
    )
  )

  (define (memoized f)
    (begin
      (define cache (make-dict))
      (lambda (n)
        (let ((res (dict-get cache n)))
          (if (not (=? res nil))
            res
            (let ((out (f n)))
              (begin (dict-set cache n out) out)
            )
          )
        )
      )
    )
  )

  (define (fib n) (if (< n 2) n (+ (fib (- n 1)) (fib (- n 2)))))
  ;(define fib (memoized fib))
)
