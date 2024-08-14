from dolibs import skintemp as sk
def test_skintemp():
    assert sk.get_n_save(1990,1,'/tmp/pytmp',['01'])
    
    
def test_del_skintemp():
    assert sk.del_image('xxxx','2023-01-01','2023-02-01')  