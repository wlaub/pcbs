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
    Port ( 
	        CLK1 : in  STD_LOGIC;
           INPUT1 : in  STD_LOGIC;
           OUTPUT1 : out  STD_LOGIC;
			  OE1 : in  STD_LOGIC;
			  
			  EXT_CLK : in STD_LOGIC;
			  CLK_SEL : in STD_LOGIC;

			  CLK2 : in  STD_LOGIC;
           INPUT2 : in  STD_LOGIC;
           OUTPUT2 : out  STD_LOGIC;
			  OE2 : in  STD_LOGIC;		  
			  
			  SCK : in STD_LOGIC;
			  SDATA : in STD_LOGIC
           );			  
end main;


architecture Behavioral of main is
	signal reg1: std_logic_vector(15 downto 0);
	signal reg2: std_logic_vector(15 downto 0);
	signal tap_reg: std_logic_vector(15 downto 0);
	signal fb1: STD_LOGIC;
	signal fb2: STD_LOGIC;
	signal int_clk1: STD_LOGIC;
begin

	
	process(reg1, INPUT1, tap_reg) is
		variable tmp : std_logic;
	begin
	 tmp := INPUT1;
    for I in 15 downto 0 loop
        tmp := tmp xor (reg1(I) and tap_reg(I));
    end loop;
    fb1 <= tmp;
	end process;
				
   int_clk1 <= CLK1 when CLK_SEL = '0' else EXT_CLK;
	process (int_clk1)
	begin
		if int_clk1'event and int_clk1='1' then  
			reg1 <= reg1(16-2 downto 0) & fb1;
		end if;
	end process;
	OUTPUT1 <= fb1 when OE1 = '1' else '0';

	process(reg2, INPUT2, tap_reg) is
		variable tmp : std_logic;
	begin
	 tmp := INPUT2;
    for I in 15 downto 0 loop
        tmp := tmp xor (reg2(I) and tap_reg(I));
    end loop;
    fb2 <= tmp;
	end process;

	process (CLK2)
	begin
		if CLK2'event and CLK2='1' then  
			reg2 <= reg2(16-2 downto 0) & fb2;
		end if;
	end process;
	OUTPUT2 <= fb2 when OE2 = '1' else '0';	
	
	process (SCK)
	begin 
		if SCK'event and SCK='1' then  
			tap_reg <= tap_reg(16-2 downto 0) & SDATA;
		end if;
	end process;
		
	
end Behavioral;

