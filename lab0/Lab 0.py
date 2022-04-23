kernel=[5,5,5,5,5,
        5,5,5,5,5,
        5,5,5,5,5,
        5,5,5,5,5,
        5,5,5,5,5
        ]
kernel_height=int((len(kernel))**(1/2))
kerneling_size=(kernel_height-1)//2

print(kernel_height,kerneling_size)
