(begin
    (define (make-account balance)
        (begin
            (define (deposit n) (set! balance (+ balance n)))
            (define (check) balance)
            (list deposit check)
        )
    )

    (define acct1 (make-account 100))
    (define dep1 (car acct1))
    (define bal1 (car (cdr acct1)))

    (define acct2 (make-account 1000000))
    (define dep2 (car acct2))
    (define bal2 (car (cdr acct2)))
)
