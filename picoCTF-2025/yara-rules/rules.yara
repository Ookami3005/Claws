/*
   YARA Rule Set
   Author: yarGen Rule Generator
   Date: 2025-03-17
   Identifier: .
   Reference: https://github.com/Neo23x0/yarGen
*/

/* Rule Set ----------------------------------------------------------------- */

rule unpacked {
   meta:
      description = ". - file unpacked.exe"
      author = "yarGen Rule Generator"
      reference = "https://github.com/Neo23x0/yarGen"
      date = "2025-03-17"
      hash1 = "16b27034cb48820e42fbea1f401e627b8bd1678fca35cc405b100225613e8685"
   strings:
      $s1 = "[FATAL ERROR] OpenProcessToken failed." fullword wide
      $s2 = "[FATAL ERROR] Failed to create the Mutex." fullword wide
      $s3 = "Failed to terminate the debugger process." fullword wide
      $s4 = "[FATAL ERROR]  Unable to create the child process." fullword wide
      $s5 = "        <requestedExecutionLevel level='asInvoker' uiAccess='false' />" fullword ascii
      $s6 = "Debugger process terminated successfully." fullword wide
      $s7 = "The debugger was detected but our process wasn't able to fight it. Exiting the program." fullword wide
      $s8 = "Our process detected the debugger and was able to fight it. Don't be surprised if the debugger crashed." fullword wide
      $s9 = "[FATAL ERROR] LookupPrivilegeValue failed." fullword wide
      $s10 = "[ERROR] Exactly two arguments expected by the Child process. Exiting..." fullword wide
      $s11 = "(Ignore) error related to Ntdll. Falling back." fullword wide
      $s12 = "- Your rules should work even if this binary is packed (or unpacked)." fullword wide
      $s13 = "[FATAL ERROR] AdjustTokenPrivileges failed." fullword wide
      $s14 = "This is a fake malware. It means no harm." fullword wide
      $s15 = "Oops! Debugger Detected. Fake malware will try to hide itself (but not really)." fullword wide
      $s16 = ".data$rs" fullword ascii
      $s17 = "- To develop an effective YARA rule, find any suspicious Win32 API functions that are being used by this program." fullword wide
      $s18 = "  <trustInfo xmlns=\"urn:schemas-microsoft-com:asm.v3\">" fullword ascii
      $s19 = "  Welcome to the YaraRules0x100 challenge!" fullword ascii
      $s20 = "[FATAL ERROR] CreateToolhelp32Snapshot failed." fullword wide
   condition:
      uint16(0) == 0x5a4d and
      9 of them
}

rule __packed {
   meta:
      description = ". - file packed.exe"
      author = "yarGen Rule Generator"
      reference = "https://github.com/Neo23x0/yarGen"
      date = "2025-03-17"
      hash1 = "1be9a04fe2e40e8f8244b860ec855df5e491603d2cc87382972a4729e54e7925"
   strings:
      $s1 = "        <requestedExecutionLevel level='asInvoker' uiAccess='false' />" fullword ascii
      $s2 = "InformationProcess/" fullword ascii
      $s3 = "(kMutex" fullword ascii
      $s4 = "GetCurrent`Id" fullword ascii
      $s5 = "  <trustInfo xmlns=\"urn:schemas-microsoft-com:asm.v3\">" fullword ascii
      $s6 = "LookupPriv" fullword ascii
      $s7 = "0X_configt" fullword ascii
      $s8 = "rray new s" fullword ascii
      $s9 = "spatch" fullword ascii
      $s10 = "PlacwG4" fullword ascii
      $s11 = "atherr" fullword ascii
      $s12 = "  </trustInfo>" fullword ascii
      $s13 = "Toolhelp3x" fullword ascii
      $s14 = "backRcrt" fullword ascii
      $s15 = "z5nIOn?" fullword ascii
      $s16 = "ideChar" fullword ascii
      $s17 = "2Snapsho" fullword ascii
      $s18 = "NtQuery" fullword ascii
      $s19 = "&ExitCo9" fullword ascii
      $s20 = "eModuleFileNameWR" fullword ascii
   condition:
      uint16(0) == 0x5a4d and
      9 of them
}

