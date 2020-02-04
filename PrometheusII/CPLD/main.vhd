----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    12:24:20 10/14/2019 
-- Design Name: 
-- Module Name:    main - Behavioral 
-- Project Name: 
-- Target DeviWEs: 
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
use IEEE.numeric_std.all;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity main is
    Port ( 
	        CLK0 : in  STD_LOGIC;
           INPUT0 : in  STD_LOGIC;
           OUTPUT0 : out  STD_LOGIC;
			  
			  EXT_CLK : in STD_LOGIC;
			  CLK_SEL : in STD_LOGIC;

			  CLK1 : in  STD_LOGIC;
           INPUT1 : in  STD_LOGIC;
           OUTPUT1 : out  STD_LOGIC;  
			  
           IO : in std_logic_vector(6 downto 0);
           
			  WE : in STD_LOGIC;
			  SDO : out STD_LOGIC;
			  SCK : in STD_LOGIC;
			  SDI : in STD_LOGIC
           );			  
end main;


architecture Behavioral of main is
   constant LEN : integer := 11; --actual length - 1 for convenienWE
   constant SLEN : integer := 11;

	signal reg0: std_logic_vector(LEN downto 0) := (others => '0');
	signal reg1: std_logic_vector(LEN downto 0) := (others => '0');
	signal tap_reg: std_logic_vector(LEN+2 downto 0) := (others => '0');
	signal fb0: STD_LOGIC;
	signal fb1: STD_LOGIC;
	signal int_CLK0: STD_LOGIC;
	signal out_reg: std_logic_vector(SLEN downto 0) := (others => '0');
	signal status_reg: std_logic_vector(SLEN downto 0);
   signal oe: std_logic_vector(1 downto 0);
begin
	
	process(reg0, INPUT0, tap_reg) is
		variable tmp : std_logic;
	begin
	 tmp := INPUT0;
    for I in LEN downto 0 loop
        tmp := tmp xor (reg0(I) and tap_reg(I));
    end loop;
    fb0 <= tmp;
	end process;
				
   int_CLK0 <= CLK0 when CLK_SEL = '0' else EXT_CLK;
	process (int_CLK0)
	begin
		if OE(0) = '1' and int_CLK0'event and int_CLK0='1' then  
			reg0 <= reg0(LEN-1 downto 0) & fb0;
		end if;
	end process;
	OUTPUT0 <= fb0 when OE(0) = '1' else '0';

	process(reg1, INPUT1, tap_reg) is
		variable tmp : std_logic;
	begin
	 tmp := INPUT1;
    for I in LEN downto 0 loop
        tmp := tmp xor (reg1(I) and tap_reg(I));
    end loop;
    fb1 <= tmp;
	end process;

	process (CLK1)
	begin
		if OE(1) = '1' and CLK1'event and CLK1='1' then  
			reg1 <= reg1(LEN-1 downto 0) & fb1;
		end if;
	end process;
	OUTPUT1 <= fb1 when OE(1) = '1' else '0';	

	process (SCK, WE)
	begin 
	  if WE='1' then  
       out_reg(10 downto 4) <= IO;
		 out_reg(11) <= CLK_SEL;
	    if SCK'event and SCK='1' then  
         tap_reg <= tap_reg(LEN+1 downto 0) & SDI;	
       end if;
     else
       oe <= tap_reg(LEN+2 downto LEN+1);
	    if SCK'event and SCK='1' then  
         out_reg <= out_reg(SLEN-1 downto 0) & '0';
       end if;
     end if;
	end process;
	SDO <= out_reg(SLEN);
		
	
end Behavioral;

