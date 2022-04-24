(begin
    (define (deriv f dx)
        (lambda (x) (/ (- (f (+ x dx)) (f (- x dx))) (* 2 dx)))
    )
    (define (foo x) (* 3 x x x))
    (define df (deriv foo 1e-3))
    (define ddf (deriv df 1e-3))
)
