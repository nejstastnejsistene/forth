: A 65 ;
: Z A 25 + ;
: a A 32 + ;
: z a 25 + ;

: is_uppercase ( char -- bool ) ord dup A >= swap Z <= and ; 
: is_lowercase ( char -- bool ) ord dup a >= swap z <= and ; 

: rot13 ( char -- pune )
    dup is_uppercase if ord A - 13 + 26 mod A + chr then else
    dup is_lowercase if ord a - 13 + 26 mod a + chr then else ;

: run , dup 0 = if then rot13 . run else ; run
