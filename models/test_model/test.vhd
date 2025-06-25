library ieee;
use ieee.std_logic_1164.all;


entity test is port(
    a, b : in std_logic;
    y : out std_logic
);
end test;

architecture behaviour of test is
begin 

    y <= a and b;

end behaviour;
