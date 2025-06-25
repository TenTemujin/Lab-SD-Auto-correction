library ieee;
use ieee.std_logic_1164.all;

entity testbench is end;

architecture behavioral is 

    signal as : std_logic := '0';
    signal bs : std_logic := '0';

begin 

    as <= not as after 5 ns;
    bs <= not bs after 10 ns;

end behavioral;
