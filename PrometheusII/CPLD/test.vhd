--------------------------------------------------------------------------------
-- Company: 
-- Engineer:
--
-- Create Date:   20:05:51 02/02/2020
-- Design Name:   
-- Module Name:   C:/Users/Gravyman3321/Documents/xilinx/lfsr/test.vhd
-- Project Name:  lfsr
-- Target Device:  
-- Tool versions:  
-- Description:   
-- 
-- VHDL Test Bench Created by ISE for module: main
-- 
-- Dependencies:
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
--
-- Notes: 
-- This testbench has been automatically generated using types std_logic and
-- std_logic_vector for the ports of the unit under test.  Xilinx recommends
-- that these types always be used for the top-level I/O of a design in order
-- to guarantee that the testbench will bind correctly to the post-implementation 
-- simulation model.
--------------------------------------------------------------------------------
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
 
-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--USE ieee.numeric_std.ALL;
 
ENTITY test IS
END test;
 
ARCHITECTURE behavior OF test IS 
 
    -- Component Declaration for the Unit Under Test (UUT)
 
    COMPONENT main
    PORT(
         CLK0 : IN  std_logic;
         INPUT0 : IN  std_logic;
         OUTPUT0 : OUT  std_logic;
         EXT_CLK : IN  std_logic;
         CLK_SEL : IN  std_logic;
         CLK1 : IN  std_logic;
         INPUT1 : IN  std_logic;
         OUTPUT1 : OUT  std_logic;
         IO : IN  std_logic_vector(6 downto 0);
         WE : IN  std_logic;
         SDO : OUT  std_logic;
         SCK : IN  std_logic;
         SDI : IN  std_logic
        );
    END COMPONENT;
    

   --Inputs
   signal CLK0 : std_logic := '0';
   signal INPUT0 : std_logic := '1';
   signal EXT_CLK : std_logic := '0';
   signal CLK_SEL : std_logic := '0';
   signal CLK1 : std_logic := '0';
   signal INPUT1 : std_logic := '1';
   signal IO : std_logic_vector(6 downto 0) := (others => '1');
   signal WE : std_logic := '0';
   signal SCK : std_logic := '0';
   signal SDI : std_logic := '0';

 	--Outputs
   signal OUTPUT0 : std_logic;
   signal OUTPUT1 : std_logic;
   signal SDO : std_logic;

   -- Clock period definitions
   constant CLK0_period : time := 200 ns;
   constant EXT_CLK_period : time := 250 ns;
   constant CLK1_period : time := 300 ns;
   constant brate : time := 1000 ns;
 
BEGIN
 
	-- Instantiate the Unit Under Test (UUT)
   uut: main PORT MAP (
          CLK0 => CLK0,
          INPUT0 => INPUT0,
          OUTPUT0 => OUTPUT0,
          EXT_CLK => EXT_CLK,
          CLK_SEL => CLK_SEL,
          CLK1 => CLK1,
          INPUT1 => INPUT1,
          OUTPUT1 => OUTPUT1,
          IO => IO,
          WE => WE,
          SDO => SDO,
          SCK => SCK,
          SDI => SDI
        );

   -- Clock process definitions
   CLK0_process :process
   begin
		CLK0 <= '0';
		wait for CLK0_period/2;
		CLK0 <= '1';
		wait for CLK0_period/2;
   end process;
 
   EXT_CLK_process :process
   begin
		EXT_CLK <= '0';
		wait for EXT_CLK_period/2;
		EXT_CLK <= '1';
		wait for EXT_CLK_period/2;
   end process;
 
   CLK1_process :process
   begin
		CLK1 <= '0';
		wait for CLK1_period/2;
		CLK1 <= '1';
		wait for CLK1_period/2;
   end process;
 

   -- Stimulus process
   stim_proc: process
   begin		
      -- hold reset state for 100 ns.
      wait for 100 ns;	

      wait for CLK0_period*10;

      -- insert stimulus here 
      WE <= '1';
      wait for brate;
      SDI <= '1'; --oe1
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '1'; --oe0
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --11
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --10
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --9
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --8
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --7
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --6
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --5
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --4
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --3
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --2
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '1'; --1
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --0
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --0
      WE <= '0';
      wait for brate;
      WE <= '1';
      wait for brate;
      WE <= '0';

      --shift io out
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      wait for brate;
      WE <= '1';

      --switch clock source
      CLK_SEL <= '1';

      ---change taps
      -- insert stimulus here 
      WE <= '1';
      wait for brate;
      SDI <= '1'; --oe1
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '1'; --oe0
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --11
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --10
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --9
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --8
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --7
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --6
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --5
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '1'; --4
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --3
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --2
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '1'; --1
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --0
      wait for brate;
      SCK <= '1';
      wait for brate;
      SCK <= '0';
      SDI <= '0'; --0
      WE <= '0';
      wait for brate;
      WE <= '1';
      wait for brate;
      WE <= '0';
      
      wait;
   end process;

END;
