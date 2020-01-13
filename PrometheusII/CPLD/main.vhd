----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    12:24:20 10/14/2019 
-- Design Name: 
-- Module Name:    main - Behavioral 
-- Project Name: 
-- Target Devices: 
-- Tool versions: 
-- Description: 
--
-- Dependencies: 
--
-- Revision: 
-- Revision 0.01 - File Created
-- Additional Comments: 
--
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity main is
    Port ( CLK : in  STD_LOGIC;
           INPUT : in  STD_LOGIC;
           OUTPUT : out  STD_LOGIC;
           TAPS : in  STD_LOGIC_VECTOR (15 downto 0));
end main;


architecture Behavioral of main is
	signal reg: std_logic_vector(15 downto 0);
	signal fb: STD_LOGIC;
begin

	process(reg, INPUT, TAPS) is
		variable tmp : std_logic;
	begin
	 tmp := INPUT;
    for I in 15 downto 0 loop
        tmp := tmp xor (reg(I) and TAPS(I));
    end loop;
    fb <= tmp;
	end process;
				
	process (CLK)
	begin
		if CLK'event and CLK='1' then  
			reg <= reg(16-2 downto 0) & fb;
		end if;
	end process;
	OUTPUT <= fb;
	
end Behavioral;

