from Crypto.Cipher import ARC4, DES # pycryptodome
from Crypto.Hash import MD5
from Crypto.Random import get_random_bytes
import base64

class WTVNetworkSecurity():
	initial_shared_key = b''
	current_shared_key = b''
	incarnation = 1
	session_key1 = b''
	session_key2 = b''
	hRC4_Key1 = None
	hRC4_Key2 = None

	def __init__(self, wtv_initial_key, wtv_incarnation = 1):
		initial_key = base64.b64decode(wtv_initial_key)

		if len(initial_key) == 8:
			self.incarnation = wtv_incarnation
			self.initial_shared_key =  initial_key
			self.current_shared_key = initial_key
		else:
			raise Exception("Invalid initial key length")

	def set_incarnation(self, wtv_incarnation):
		self.incarnation = wtv_incarnation

	def increment_incarnation(self):
		self.incarnation = self.incarnation + 1

	"""
	ROM:8049A310 Network__ProcessChallenge:               # CODE XREF: Network__SetHeader+210↓p
	ROM:8049A310
	ROM:8049A310 var_E8          = -0xE8
	ROM:8049A310 var_E0          = -0xE0
	ROM:8049A310 var_60          = -0x60
	ROM:8049A310 var_50          = -0x50
	ROM:8049A310 var_40          = -0x40
	ROM:8049A310 var_38          = -0x38
	ROM:8049A310 var_34          = -0x34
	ROM:8049A310 var_30          = -0x30
	ROM:8049A310 var_28          = -0x28
	ROM:8049A310 var_24          = -0x24
	ROM:8049A310 var_20          = -0x20
	ROM:8049A310 var_1C          = -0x1C
	ROM:8049A310 var_18          = -0x18
	ROM:8049A310 var_14          = -0x14
	ROM:8049A310 var_10          = -0x10
	ROM:8049A310 var_C           = -0xC
	ROM:8049A310 var_8           = -8
	ROM:8049A310 var_4           = -4
	ROM:8049A310 arg_42          =  0x42
	ROM:8049A310 arg_43          =  0x43
	ROM:8049A310
	ROM:8049A310                 addiu   $sp, -0xF8
	ROM:8049A314                 sw      $fp, 0xF8+var_8($sp)
	ROM:8049A318                 sw      $s3, 0xF8+var_1C($sp)
	ROM:8049A31C                 sw      $s2, 0xF8+var_20($sp)
	ROM:8049A320                 sw      $s1, 0xF8+var_24($sp)
	ROM:8049A324                 sw      $s0, 0xF8+var_28($sp)
	ROM:8049A328                 sw      $ra, 0xF8+var_4($sp)
	ROM:8049A32C                 sw      $s7, 0xF8+var_C($sp)
	ROM:8049A330                 sw      $s6, 0xF8+var_10($sp)
	ROM:8049A334                 sw      $s5, 0xF8+var_14($sp)
	ROM:8049A338                 sw      $s4, 0xF8+var_18($sp)
	ROM:8049A33C                 move    $fp, $a0
	ROM:8049A340                 move    $s0, $a1
	ROM:8049A344                 sw      $zero, 0xF8+var_30($sp)
	ROM:8049A348                 move    $s2, $zero
	ROM:8049A34C                 move    $s3, $zero
	ROM:8049A350                 bnez    $s0, loc_8049A364
	ROM:8049A354                 move    $s1, $zero
	ROM:8049A358                 break   0
	ROM:8049A35C                 j       loc_8049A5CC
	ROM:8049A360                 li      $v0, 0xFFFFFFFF
	ROM:8049A364  # ---------------------------------------------------------------------------
	ROM:8049A364
	ROM:8049A364 loc_8049A364:                            # CODE XREF: Network__ProcessChallenge+40↑j
	ROM:8049A364                 lbu     $v0, 0xF8+arg_42($fp)
	ROM:8049A368                 bnez    $v0, loc_8049A37C
	ROM:8049A36C                 addiu   $a0, $sp, 0xF8+var_E0
	ROM:8049A370                 break   0
	ROM:8049A374                 j       loc_8049A5CC
	ROM:8049A378                 li      $v0, 0xFFFFFFE9
	ROM:8049A37C  # ---------------------------------------------------------------------------
	ROM:8049A37C
	ROM:8049A37C loc_8049A37C:                            # CODE XREF: Network__ProcessChallenge+58↑j
	ROM:8049A37C                 move    $a1, $zero
	ROM:8049A380                 jal     wtv_memset
	ROM:8049A384                 li      $a2, 0xA4
	ROM:8049A388                 jal     wtv_strlen
	ROM:8049A38C                 move    $a0, $s0
	ROM:8049A390                 sw      $v0, 0xF8+var_38($sp)
	ROM:8049A394                 move    $a0, $s0
	ROM:8049A398                 jal     FNewFromBase64
	ROM:8049A39C                 addiu   $a1, $sp, 0xF8+var_38
	ROM:8049A3A0                 move    $s7, $v0
	ROM:8049A3A4                 beqz    $s7, loc_8049A578
	ROM:8049A3A8                 lui     $a0, 0x806D
	ROM:8049A3AC                 jal     AllocateMemorySystem
	ROM:8049A3B0                 lw      $a0, 0xF8+var_38($sp)
	ROM:8049A3B4                 move    $s2, $v0
	ROM:8049A3B8                 beqz    $s2, loc_8049A574
	ROM:8049A3BC                 move    $a0, $s2
	ROM:8049A3C0                 move    $a1, $s7
	ROM:8049A3C4                 jal     wtv_memcpy
	ROM:8049A3C8                 li      $a2, 8
	ROM:8049A3CC                 lui     $t0, 0x8000
	ROM:8049A3D0                 addiu   $s6, $fp, 0xF8+var_40
	ROM:8049A3D4                 addiu   $v0, $s2, 8
	ROM:8049A3D8                 lw      $a1, 0x8000587C
	ROM:8049A3DC                 move    $s4, $v0
	ROM:8049A3E0                 addiu   $a0, $sp, 0xF8+var_E0
	ROM:8049A3E4                 move    $a2, $s6
	ROM:8049A3E8                 jal     EVP_DecryptInit
	ROM:8049A3EC                 move    $a3, $zero
	ROM:8049A3F0                 lw      $v0, 0xF8+var_38($sp)
	ROM:8049A3F4                 addiu   $s5, $sp, 0xF8+var_34
	ROM:8049A3F8                 addiu   $v0, -8
	ROM:8049A3FC                 addiu   $a0, $sp, 0xF8+var_E0
	ROM:8049A400                 sw      $v0, 0xF8+var_E8($sp)
	ROM:8049A404                 move    $a1, $s4
	ROM:8049A408                 move    $a2, $s5
	ROM:8049A40C                 jal     EVP_DecryptUpdate
	ROM:8049A410                 addiu   $a3, $s7, 8
	ROM:8049A414                 lw      $s0, 0xF8+var_34($sp)
	ROM:8049A418                 addiu   $a0, $sp, 0xF8+var_E0
	ROM:8049A41C                 addu    $a1, $s4, $s0
	ROM:8049A420                 jal     EVP_DecryptFinal
	ROM:8049A424                 move    $a2, $s5
	ROM:8049A428                 lw      $v0, 0xF8+var_34($sp)
	ROM:8049A42C                 li      $v1, 0x60
	ROM:8049A430                 addu    $s0, $v0
	ROM:8049A434                 bne     $s0, $v1, loc_8049A578
	ROM:8049A438                 lui     $a0, 0x806D
	ROM:8049A43C                 move    $a0, $s4
	ROM:8049A440                 li      $a1, 0x50
	ROM:8049A444                 jal     MD5
	ROM:8049A448                 move    $a2, $zero
	ROM:8049A44C                 move    $a0, $v0
	ROM:8049A450                 addiu   $a1, $s2, 0x58
	ROM:8049A454                 jal     wtv_memcmp
	ROM:8049A458                 li      $a2, 0x10
	ROM:8049A45C                 beqz    $v0, loc_8049A46C
	ROM:8049A460                 li      $t0, 0xFFFFFFE9
	ROM:8049A464                 j       loc_8049A588
	ROM:8049A468                 sw      $t0, 0xF8+var_30($sp)
	ROM:8049A46C  # ---------------------------------------------------------------------------
	ROM:8049A46C
	ROM:8049A46C loc_8049A46C:                            # CODE XREF: Network__ProcessChallenge+14C↑j
	ROM:8049A46C                 addiu   $a0, $fp, 0xF8+var_60 ; ERIC: referenced in 80497AEC:Network__GetSessionKey1 (var_60=0x60, 0xF8 - 0x60 = 0x98)
	ROM:8049A470                 addiu   $a1, $s2, 0x30
	ROM:8049A474                 jal     wtv_memcpy
	ROM:8049A478                 li      $a2, 0x10
	ROM:8049A47C                 addiu   $a0, $fp, 0xF8+var_50 ; ERIC: referenced in 80497B60:Network__GetSessionKey2 (var_50=0x50, 0xF8 - 0x50 = 0xa8)
	ROM:8049A480                 addiu   $a1, $s2, 0x40
	ROM:8049A484                 jal     wtv_memcpy
	ROM:8049A488                 li      $a2, 0x10
	ROM:8049A48C                 move    $a0, $s6
	ROM:8049A490                 addiu   $a1, $s2, 0x50
	ROM:8049A494                 jal     wtv_memcpy
	ROM:8049A498                 li      $a2, 8
	ROM:8049A49C                 li      $v0, 1
	ROM:8049A4A0                 sb      $v0, 0xF8+arg_43($fp)
	ROM:8049A4A4                 sb      $v0, 0xF8+arg_42($fp)
	ROM:8049A4A8                 jal     AllocateMemorySystem
	ROM:8049A4AC                 li      $a0, 0x48
	ROM:8049A4B0                 move    $s3, $v0
	ROM:8049A4B4                 beqz    $s3, loc_8049A574
	ROM:8049A4B8                 move    $a0, $s3
	ROM:8049A4BC                 move    $a1, $s2
	ROM:8049A4C0                 jal     wtv_memcpy
	ROM:8049A4C4                 li      $a2, 8
	ROM:8049A4C8                 addiu   $a0, $s3, 0x18
	ROM:8049A4CC                 move    $a1, $s4
	ROM:8049A4D0                 li      $a2, 0x28
	ROM:8049A4D4                 jal     wtv_memcpy
	ROM:8049A4D8                 addiu   $s1, $s3, 8
	ROM:8049A4DC                 move    $a2, $s1
	ROM:8049A4E0                 move    $a0, $s4
	ROM:8049A4E4                 jal     MD5
	ROM:8049A4E8                 li      $a1, 0x28
	ROM:8049A4EC                 addiu   $a0, $sp, 0xF8+var_E0
	ROM:8049A4F0                 move    $a1, $zero
	ROM:8049A4F4                 jal     wtv_memset
	ROM:8049A4F8                 li      $a2, 0xA4
	ROM:8049A4FC                 lui     $t0, 0x8000
	ROM:8049A500                 lw      $a1, 0x8000587C
	ROM:8049A504                 move    $a2, $s6
	ROM:8049A508                 addiu   $a0, $sp, 0xF8+var_E0
	ROM:8049A50C                 jal     EVP_EncryptInit
	ROM:8049A510                 move    $a3, $zero
	ROM:8049A514                 li      $v0, 0x38
	ROM:8049A518                 move    $a1, $s1
	ROM:8049A51C                 move    $a3, $s1
	ROM:8049A520                 sw      $v0, 0xF8+var_E8($sp)
	ROM:8049A524                 addiu   $a0, $sp, 0xF8+var_E0
	ROM:8049A528                 jal     EVP_EncryptUpdate
	ROM:8049A52C                 move    $a2, $s5
	ROM:8049A530                 lw      $s0, 0xF8+var_34($sp)
	ROM:8049A534                 move    $a2, $s5
	ROM:8049A538                 addu    $a1, $s1, $s0
	ROM:8049A53C                 addiu   $s0, 8
	ROM:8049A540                 jal     EVP_EncryptFinal
	ROM:8049A544                 addiu   $a0, $sp, 0xF8+var_E0
	ROM:8049A548                 lw      $a1, 0xF8+var_34($sp)
	ROM:8049A54C                 move    $a0, $s3
	ROM:8049A550                 jal     FNewBase64StringFromBuf
	ROM:8049A554                 addu    $a1, $s0, $a1
	ROM:8049A558                 move    $s1, $v0
	ROM:8049A55C                 beqz    $s1, loc_8049A574
	ROM:8049A560                 move    $a0, $fp
	ROM:8049A564                 jal     Network__SetResponse
	ROM:8049A568                 move    $a1, $s1
	ROM:8049A56C                 j       loc_8049A588
	ROM:8049A570                 nop
	ROM:8049A574  # ---------------------------------------------------------------------------
	ROM:8049A574
	ROM:8049A574 loc_8049A574:                            # CODE XREF: Network__ProcessChallenge+A8↑j
	ROM:8049A574                                          # Network__ProcessChallenge+1A4↑j ...
	ROM:8049A574                 lui     $a0, 0x806D
	ROM:8049A578
	ROM:8049A578 loc_8049A578:                            # CODE XREF: Network__ProcessChallenge+94↑j
	ROM:8049A578                                          # Network__ProcessChallenge+124↑j
	ROM:8049A578                 li      $t0, 0xFFFFFFFF
	ROM:8049A57C                 addiu   $a0, (aProcesschallen - 0x806D0000)  # "ProcessChallenge Error"
	ROM:8049A580                 jal     DoMessage
	ROM:8049A584                 sw      $t0, 0xF8+var_30($sp)
	ROM:8049A588
	ROM:8049A588 loc_8049A588:                            # CODE XREF: Network__ProcessChallenge+154↑j
	ROM:8049A588                                          # Network__ProcessChallenge+25C↑j
	ROM:8049A588                 beqz    $s3, loc_8049A598
	ROM:8049A58C                 nop
	ROM:8049A590                 jal     FreeMemorySystem
	ROM:8049A594                 move    $a0, $s3
	ROM:8049A598
	ROM:8049A598 loc_8049A598:                            # CODE XREF: Network__ProcessChallenge:loc_8049A588↑j
	ROM:8049A598                 beqz    $s7, loc_8049A5A8
	ROM:8049A59C                 nop
	ROM:8049A5A0                 jal     FreeMemorySystem
	ROM:8049A5A4                 move    $a0, $s7
	ROM:8049A5A8
	ROM:8049A5A8 loc_8049A5A8:                            # CODE XREF: Network__ProcessChallenge:loc_8049A598↑j
	ROM:8049A5A8                 beqz    $s2, loc_8049A5B8
	ROM:8049A5AC                 nop
	ROM:8049A5B0                 jal     FreeMemorySystem
	ROM:8049A5B4                 move    $a0, $s2
	ROM:8049A5B8
	ROM:8049A5B8 loc_8049A5B8:                            # CODE XREF: Network__ProcessChallenge:loc_8049A5A8↑j
	ROM:8049A5B8                 beqz    $s1, loc_8049A5CC
	ROM:8049A5BC                 lw      $v0, 0xF8+var_30($sp)
	ROM:8049A5C0                 jal     FreeMemorySystem
	ROM:8049A5C4                 move    $a0, $s1
	ROM:8049A5C8                 lw      $v0, 0xF8+var_30($sp)
	ROM:8049A5CC
	ROM:8049A5CC loc_8049A5CC:                            # CODE XREF: Network__ProcessChallenge+4C↑j
	ROM:8049A5CC                                          # Network__ProcessChallenge+64↑j ...
	ROM:8049A5CC                 lw      $ra, 0xF8+var_4($sp)
	ROM:8049A5D0                 lw      $fp, 0xF8+var_8($sp)
	ROM:8049A5D4                 lw      $s7, 0xF8+var_C($sp)
	ROM:8049A5D8                 lw      $s6, 0xF8+var_10($sp)
	ROM:8049A5DC                 lw      $s5, 0xF8+var_14($sp)
	ROM:8049A5E0                 lw      $s4, 0xF8+var_18($sp)
	ROM:8049A5E4                 lw      $s3, 0xF8+var_1C($sp)
	ROM:8049A5E8                 lw      $s2, 0xF8+var_20($sp)
	ROM:8049A5EC                 lw      $s1, 0xF8+var_24($sp)
	ROM:8049A5F0                 lw      $s0, 0xF8+var_28($sp)
	ROM:8049A5F4                 jr      $ra
	ROM:8049A5F8                 addiu   $sp, 0xF8
	ROM:8049A5F8  # End of function Network__ProcessChallenge
	"""
	def ProcessChallenge(self, wtv_challenge):
		challenge = base64.b64decode(wtv_challenge)

		if len(challenge) > 8:
			hDES1 = DES.new(self.current_shared_key, DES.MODE_ECB)
			challenge_decrypted = hDES1.decrypt(challenge[8:])

			hMD5 = MD5.new()
			hMD5.update(challenge_decrypted[0:80])

			if challenge_decrypted[80:96] == hMD5.digest():
				self.current_shared_key = challenge_decrypted[72:80]

				challenge_echo = challenge_decrypted[0:40]
				hMD5 = MD5.new()
				hMD5.update(challenge_echo)
				challenge_echo_md5 = hMD5.digest()

				# RC4 encryption keys.  Stored in the wtv-ticket on the server side.
				self.session_key1 = challenge_decrypted[40:56]
				self.session_key2 = challenge_decrypted[56:72]

				hDES2 = DES.new(self.current_shared_key, DES.MODE_ECB)
				echo_encrypted = hDES2.encrypt(challenge_echo_md5 + challenge_echo)

				# Last bytes is just extra padding
				challenge_response = challenge[0:8] + echo_encrypted + (b'\x00' * 8)


				return str(base64.b64encode(challenge_response), "ascii")
			else:
				raise Exception("Couldn't solve challenge")

			return ""
		else:
			raise Exception("Invalid challenge length")

	def IssueChallenge(self):
		# bytes 0-8: Random id?  Just echoed in the response
		# bytes 8-XX: DES encrypted block.  Encrypted with the initial key or subsequent keys from the challenge.
		#	bytes 8-48: hidden random data we echo back in the response
		#	bytes 48-64: session key 1 used in RC4 encryption triggered by SECURE ON
		#	bytes 64-80: session key 2 used in RC4 encryption triggered by SECURE ON
		#	bytes 80-88: new key for future challenges
		#	bytes 88-104: MD5 of 8-88
		#	bytes 104-112: padding. not important

		random_id_question_mark = get_random_bytes(8)

		echo_me = get_random_bytes(40)
		self.session_key1 = get_random_bytes(16)
		self.session_key2 = get_random_bytes(16)
		new_shared_key = get_random_bytes(8)

		challenge_puzzle = echo_me + self.session_key1 + self.session_key2 + new_shared_key
		hMD5 = MD5.new()
		hMD5.update(challenge_puzzle)
		challenge_puzzle_md5 = hMD5.digest()

		challenge_secret = challenge_puzzle + challenge_puzzle_md5 + (b'\x00' * 8)

		# Shhhh!!
		hDES2 = DES.new(self.current_shared_key, DES.MODE_ECB)
		challenge_secreted = hDES2.encrypt(challenge_secret)

		self.current_shared_key = new_shared_key

		challenge = random_id_question_mark + challenge_secreted

		return str(base64.b64encode(challenge), "ascii")

	"""
	ROM:804A703C WTVProtocol__SetSessionKeys:             # CODE XREF: WTVProtocol__IdleSecureEnd+E4↑p
	ROM:804A703C                                          # WTVProtocol__GetSessionKeys+28↓p
	ROM:804A703C
	ROM:804A703C var_10          = -0x10
	ROM:804A703C var_C           = -0xC
	ROM:804A703C var_8           = -8
	ROM:804A703C
	ROM:804A703C                 addiu   $sp, -0x20
	ROM:804A7040                 sw      $s1, 0x20+var_C($sp)
	ROM:804A7044                 sw      $s0, 0x20+var_10($sp)
	ROM:804A7048                 move    $s0, $a0
	ROM:804A704C                 lui     $s1, 0x8000
	ROM:804A7050                 sw      $ra, 0x20+var_8($sp)
	ROM:804A7054                 lw      $a0, 0x80001274
	ROM:804A7058                 jal     Network__GetSessionKey1
	ROM:804A705C                 lw      $a1, 0x24($s0)
	ROM:804A7060                 addiu   $a0, $s0, 0x6C ; ERIC: context for RC4 algorithm 1
	ROM:804A7064                 move    $a1, $v0 ; ERIC: MD5 return from Network__GetSessionKey1
	ROM:804A7068                 jal     RC4_Init
	ROM:804A706C                 li      $a2, 0x10 ; ERIC: size of key (MD5 digest length)
	ROM:804A7070                 lw      $a0, 0x80001274
	ROM:804A7074                 jal     Network__GetSessionKey2
	ROM:804A7078                 lw      $a1, 0x24($s0)
	ROM:804A707C                 addiu   $a0, $s0, 0x178 ; ERIC: context for RC4 algorithm 2
	ROM:804A7080                 move    $a1, $v0 ; ERIC: MD5 return from Network__GetSessionKey2
	ROM:804A7084                 jal     RC4_Init
	ROM:804A7088                 li      $a2, 0x10 ; ERIC: size of key (MD5 digest length)
	ROM:804A708C                 li      $v0, 1
	ROM:804A7090                 sb      $v0, 0x284($s0)
	ROM:804A7094                 lw      $ra, 0x20+var_8($sp)
	ROM:804A7098                 lw      $s1, 0x20+var_C($sp)
	ROM:804A709C                 lw      $s0, 0x20+var_10($sp)
	ROM:804A70A0                 move    $v0, $zero
	ROM:804A70A4                 jr      $ra
	ROM:804A70A8                 addiu   $sp, 0x20
	ROM:804A70A8  # End of function WTVProtocol__SetSessionKeys
	ROM:80497ADC Network__GetSessionKey1:                 # CODE XREF: WTVProtocol__SetSessionKeys+1C↓p
	ROM:80497ADC
	ROM:80497ADC var_40          = -0x40
	ROM:80497ADC var_30          = -0x30
	ROM:80497ADC var_2C          = -0x2C
	ROM:80497ADC var_18          = -0x18
	ROM:80497ADC var_10          = -0x10
	ROM:80497ADC var_C           = -0xC
	ROM:80497ADC var_8           = -8
	ROM:80497ADC
	ROM:80497ADC                 addiu   $sp, -0x50
	ROM:80497AE0                 sw      $s1, 0x50+var_C($sp)
	ROM:80497AE4                 sw      $s0, 0x50+var_10($sp)
	ROM:80497AE8                 move    $s0, $a1
	ROM:80497AEC                 addiu   $s1, $a0, 0x98 ; ERIC: FROM 8049A46C:Network__ProcessChallenge
	ROM:80497AF0                 move    $a1, $s1
	ROM:80497AF4                 sw      $ra, 0x50+var_8($sp)
	ROM:80497AF8                 addiu   $a0, $sp, 0x50+var_40
	ROM:80497AFC                 jal     wtv_memcpy
	ROM:80497B00                 li      $a2, 0x10
	ROM:80497B04                 sw      $s0, 0x50+var_18($sp)
	ROM:80497B08                 addiu   $a0, $sp, 0x50+var_30
	ROM:80497B0C                 addiu   $a1, $sp, 0x50+var_18 ; ERIC: wtv-incarnation number.  Incremented each time a new RC4 session starts
	ROM:80497B10                 jal     wtv_memcpy
	ROM:80497B14                 li      $a2, 4
	ROM:80497B18                 move    $a1, $s1 ; ERIC: session key repeated
	ROM:80497B1C                 addiu   $a0, $sp, 0x50+var_2C
	ROM:80497B20                 jal     wtv_memcpy
	ROM:80497B24                 li      $a2, 0x10
	ROM:80497B28                 li      $a2, 0x8000D1C8
	ROM:80497B30                 addiu   $a0, $sp, 0x50+var_40
	ROM:80497B34                 jal     MD5
	ROM:80497B38                 li      $a1, 0x24
	ROM:80497B3C                 lw      $ra, 0x50+var_8($sp)
	ROM:80497B40                 lw      $s1, 0x50+var_C($sp)
	ROM:80497B44                 lw      $s0, 0x50+var_10($sp)
	ROM:80497B48                 jr      $ra
	ROM:80497B4C                 addiu   $sp, 0x50
	ROM:80497B4C  # End of function Network__GetSessionKey1
	ROM:80497B50 Network__GetSessionKey2:                 # CODE XREF: WTVProtocol__SetSessionKeys+38↓p
	ROM:80497B50
	ROM:80497B50 var_40          = -0x40
	ROM:80497B50 var_30          = -0x30
	ROM:80497B50 var_2C          = -0x2C
	ROM:80497B50 var_18          = -0x18
	ROM:80497B50 var_10          = -0x10
	ROM:80497B50 var_C           = -0xC
	ROM:80497B50 var_8           = -8
	ROM:80497B50
	ROM:80497B50                 addiu   $sp, -0x50
	ROM:80497B54                 sw      $s1, 0x50+var_C($sp)
	ROM:80497B58                 sw      $s0, 0x50+var_10($sp)
	ROM:80497B5C                 move    $s0, $a1
	ROM:80497B60                 addiu   $s1, $a0, 0xA8 ; ERIC: FROM 8049A47C:Network__ProcessChallenge
	ROM:80497B64                 move    $a1, $s1
	ROM:80497B68                 sw      $ra, 0x50+var_8($sp)
	ROM:80497B6C                 addiu   $a0, $sp, 0x50+var_40
	ROM:80497B70                 jal     wtv_memcpy
	ROM:80497B74                 li      $a2, 0x10
	ROM:80497B78                 sw      $s0, 0x50+var_18($sp)
	ROM:80497B7C                 addiu   $a0, $sp, 0x50+var_30
	ROM:80497B80                 addiu   $a1, $sp, 0x50+var_18 ; ERIC: wtv-incarnation number.  Incremented each time a new RC4 session starts
	ROM:80497B84                 jal     wtv_memcpy
	ROM:80497B88                 li      $a2, 4
	ROM:80497B8C                 move    $a1, $s1 ; ERIC: session key repeated
	ROM:80497B90                 addiu   $a0, $sp, 0x50+var_2C
	ROM:80497B94                 jal     wtv_memcpy
	ROM:80497B98                 li      $a2, 0x10
	ROM:80497B9C                 li      $a2, 0x8000D1C8
	ROM:80497BA4                 addiu   $a0, $sp, 0x50+var_40
	ROM:80497BA8                 jal     MD5
	ROM:80497BAC                 li      $a1, 0x24
	ROM:80497BB0                 lw      $ra, 0x50+var_8($sp)
	ROM:80497BB4                 lw      $s1, 0x50+var_C($sp)
	ROM:80497BB8                 lw      $s0, 0x50+var_10($sp)
	ROM:80497BBC                 jr      $ra
	ROM:80497BC0                 addiu   $sp, 0x50
	ROM:80497BC0  # End of function Network__GetSessionKey2
	"""

	def SecureOn(self):
		hMD5 = MD5.new()
		hMD5.update(self.session_key1 + self.incarnation.to_bytes(4, byteorder='big') + self.session_key1)
		self.hRC4_Key1 = ARC4.new(hMD5.digest())

		hMD51 = MD5.new()
		hMD51.update(self.session_key2 + self.incarnation.to_bytes(4, byteorder='big') + self.session_key2)
		self.hRC4_Key2 = ARC4.new(hMD5.digest())

	def EncryptKey1(self, data):
		return self.Encrypt(self.hRC4_Key1, data)

	def EncryptKey2(self, data):
		return self.Encrypt(self.hRC4_Key2, data)

	def Encrypt(self, context, data):
		if context != None:
			return context.encrypt(data)
		else:
			raise Exception("Invalid RC4 encryption context")

	def DecryptKey1(self, data):
		return self.Decrypt(self.hRC4_Key1, data)

	def DecryptKey2(self, data):
		return self.Decrypt(self.hRC4_Key2, data)

	def Decrypt(self, context, data):
		if context != None:
			return context.decrypt(data)
		else:
			raise Exception("Invalid RC4 decryption context")


	"""
	ERIC: The RC4 stream doesn't start until "SECURE ON" is sent to the server.

	ROM:804A6DE0 WTVProtocol__IdleSecureBegin:            # DATA XREF: ROM:806D3DF4↓o
	ROM:804A6DE0
	ROM:804A6DE0 var_18          = -0x18
	ROM:804A6DE0 var_14          = -0x14
	ROM:804A6DE0 var_10          = -0x10
	ROM:804A6DE0 var_C           = -0xC
	ROM:804A6DE0 var_8           = -8
	ROM:804A6DE0
	ROM:804A6DE0                 addiu   $sp, -0x28
	ROM:804A6DE4                 sw      $s2, 0x28+var_10($sp)
	ROM:804A6DE8                 lui     $a1, 0x8000
	ROM:804A6DEC                 sw      $ra, 0x28+var_8($sp)
	ROM:804A6DF0                 sw      $s3, 0x28+var_C($sp)
	ROM:804A6DF4                 sw      $s1, 0x28+var_14($sp)
	ROM:804A6DF8                 sw      $s0, 0x28+var_18($sp)
	ROM:804A6DFC                 lw      $v1, 0x80001410
	ROM:804A6E00                 move    $s2, $a0
	ROM:804A6E04                 lw      $v0, 0x10($s2)
	ROM:804A6E08                 sw      $v1, 0x24($s2)
	ROM:804A6E0C                 lw      $v0, 4($v0)
	ROM:804A6E10                 addiu   $v1, 1
	ROM:804A6E14                 xori    $v0, 1
	ROM:804A6E18                 andi    $v0, 1
	ROM:804A6E1C                 beqz    $v0, loc_804A6EFC
	ROM:804A6E20                 sw      $v1, 0x80001410
	ROM:804A6E24                 lui     $s3, 0x8000
	ROM:804A6E28                 lw      $v1, 0x80001274
	ROM:804A6E2C                 lbu     $v0, 0x139($v1)
	ROM:804A6E30                 beqz    $v0, loc_804A6E40
	ROM:804A6E34                 move    $a0, $zero
	ROM:804A6E38                 lbu     $v0, 0x122($v1)
	ROM:804A6E3C                 sltu    $a0, $zero, $v0
	ROM:804A6E40
	ROM:804A6E40 loc_804A6E40:                            # CODE XREF: WTVProtocol__IdleSecureBegin+50↑j
	ROM:804A6E40                 beqz    $a0, loc_804A6EFC
	ROM:804A6E44                 addiu   $s0, $s2, 0x28
	ROM:804A6E48                 la      $a1, aSecureOn   # "SECURE ON"
	ROM:804A6E50                 jal     Stream__WriteString
	ROM:804A6E54                 move    $a0, $s0
	ROM:804A6E58                 la      $s1, dword_806D3AD8
	ROM:804A6E60                 move    $a0, $s0
	ROM:804A6E64                 jal     Stream__WriteString
	ROM:804A6E68                 move    $a1, $s1
	ROM:804A6E6C                 lui     $a2, 0x8000
	ROM:804A6E70                 lui     $a1, 0x806D
	ROM:804A6E74                 li      $a2, 0x800024A0
	ROM:804A6E78                 la      $a1, aAcceptLanguage_0  # "Accept-Language"
	ROM:804A6E7C                 jal     Stream__WriteAttribute
	ROM:804A6E80                 move    $a0, $s0
	ROM:804A6E84                 lw      $a0, 0x1274($s3)
	ROM:804A6E88                 lw      $v0, 4($a0)
	ROM:804A6E8C                 lw      $v0, 0xC($v0)
	ROM:804A6E90                 jalr    $v0
	ROM:804A6E94                 move    $a1, $s0
	ROM:804A6E98                 jal     System__WriteHeaders
	ROM:804A6E9C                 move    $a0, $s0
	ROM:804A6EA0                 la      $a1, aWtvIncarnation_0  # "wtv-incarnation:"
	ROM:804A6EA8                 sb      $zero, 0x1C($s2)
	ROM:804A6EAC                 jal     Stream__WriteString
	ROM:804A6EB0                 move    $a0, $s0
	ROM:804A6EB4                 lw      $a1, 0x24($s2)
	ROM:804A6EB8                 jal     Stream__WriteNumeric
	ROM:804A6EBC                 move    $a0, $s0
	ROM:804A6EC0                 move    $a0, $s0
	ROM:804A6EC4                 jal     Stream__WriteString
	ROM:804A6EC8                 move    $a1, $s1
	ROM:804A6ECC                 move    $a0, $s0
	ROM:804A6ED0                 jal     Stream__WriteString
	ROM:804A6ED4                 move    $a1, $s1
	ROM:804A6ED8                 move    $a0, $s2
	ROM:804A6EDC                 jal     Protocol__SetState
	ROM:804A6EE0                 li      $a1, 4
	ROM:804A6EE4                 lw      $v0, 0x20($s2)
	ROM:804A6EE8                 lw      $v0, 0x28($v0)
	ROM:804A6EEC                 jalr    $v0
	ROM:804A6EF0                 move    $a0, $s2
	ROM:804A6EF4                 j       loc_804A6F0C
	ROM:804A6EF8                 lw      $ra, 0x28+var_8($sp)
	ROM:804A6EFC  # ---------------------------------------------------------------------------
	ROM:804A6EFC
	ROM:804A6EFC loc_804A6EFC:                            # CODE XREF: WTVProtocol__IdleSecureBegin+3C↑j
	ROM:804A6EFC                                          # WTVProtocol__IdleSecureBegin:loc_804A6E40↑j
	ROM:804A6EFC                 move    $a0, $s2
	ROM:804A6F00                 jal     Protocol__SetState
	ROM:804A6F04                 li      $a1, 5
	ROM:804A6F08                 lw      $ra, 0x28+var_8($sp)
	ROM:804A6F0C
	ROM:804A6F0C loc_804A6F0C:                            # CODE XREF: WTVProtocol__IdleSecureBegin+114↑j
	ROM:804A6F0C                 lw      $s3, 0x28+var_C($sp)
	ROM:804A6F10                 lw      $s2, 0x28+var_10($sp)
	ROM:804A6F14                 lw      $s1, 0x28+var_14($sp)
	ROM:804A6F18                 lw      $s0, 0x28+var_18($sp)
	ROM:804A6F1C                 jr      $ra
	ROM:804A6F20                 addiu   $sp, 0x28
	ROM:804A6F20  # End of function WTVProtocol__IdleSecureBegin
	"""


################################################################################
################################################################################
################################################################################

print("Starting WTV Protocol Session")


############## STEP 1: GET INITIAL KEY
"""
200 OK
Connection: Keep-Alive
wtv-initial-key: CC5rWmRUE0o=
wtv-service: reset
wtv-service: name=wtv-head-waiter host=74.76.120.18 port=1601 flags=0x00000001 connections=1
wtv-service: name=wtv-* host=74.76.120.18 port=1603 flags=0x00000007
wtv-service: name=wtv-flashrom host=74.76.120.18 port=1618 flags=0x00000040
wtv-boot-url: wtv-head-waiter:/login?
wtv-visit: wtv-head-waiter:/login?
wtv-client-time-zone: PST -0800
wtv-client-time-dst-rule: PST
wtv-client-date: Sun, 30 May 2021 23:13:41 GMT
Content-length: 0
Content-type: text/html
"""
# Random binary data, needs to be 8 bytes.
# Generated and stored on the server, sent to the client and stored in NVRAM (with a client-generated checksum of the the key)
wtv_initial_key = "CC5rWmRUE0o="

# Start WTV networking example
# wtv-incarnation: 9
s = WTVNetworkSecurity(wtv_initial_key)

print("Initial Key: ", wtv_initial_key)

############## STEP 2: GET SESSION KEYS AND NEW KEY BY DESCRYPTING THE CHALLENGE WITH INITIAL KEY
"""
200 OK
Connection: Keep-Alive
Expires: Wed, 09 Oct 1991 22:00:00 GMT
wtv-expire-all: wtv-head-waiter:
wtv-service: name=wtv-log host=74.76.120.18 port=1609 connections=1
wtv-log-url: wtv-log:/log
wtv-challenge: 0kjyqIYAu0ziFBbSERN6DGaZ6S0fT+DBUCtpHCJ4lpuM7CbXdAm+x83BIDoJYztd1Z+5KFZ7ghmb3LJCT/6mhWUYkqqKOyfPRW8ZIdbICK/CV+Kxm8EUjRXZSk/97tsmFpH3hcCJ7C2TBw+TX38uQQ==
wtv-relogin-url: wtv-head-waiter:/login?relogin=true
wtv-reconnect-url: wtv-head-waiter:/reconnect
wtv-visit: wtv-head-waiter:/login-stage-two-wtv-token-528908376-BA0E0008F5A465EA94AF3FDD83B4F05C?
Content-length: 0
Content-type: text/html
"""
# What the client would send to the server to validate they share the same key
# Example initial challenge from the server issued at /login
wtv_challenge1 = "0kjyqIYAu0ziFBbSERN6DGaZ6S0fT+DBUCtpHCJ4lpuM7CbXdAm+x83BIDoJYztd1Z+5KFZ7ghmb3LJCT/6mhWUYkqqKOyfPRW8ZIdbICK/CV+Kxm8EUjRXZSk/97tsmFpH3hcCJ7C2TBw+TX38uQQ==";
wtv_challenge_response1 = s.ProcessChallenge(wtv_challenge1)

print("Challenge: ", wtv_challenge1)
print("Challenge Response: ", wtv_challenge_response1)
# The fluff at the end of the response isn't useful.  Reason why it's different from here.


"""
GET wtv-head-waiter:/login-stage-two-wtv-token-528908376-BA0E0008F5A465EA94AF3FDD83B4F05C?
Referer: wtv-head-waiter:/login?
wtv-request-type: primary
wtv-system-cpuspeed: 166164662
wtv-system-sysconfig: 3116068
wtv-disk-size: 8006
wtv-incarnation: 2
wtv-challenge-response: 0kjyqIYAu0zI5QrLhSuEUFgKkoVSxI3zBlUMfhnIYoMy0ExfIX4s/mHvILseDFx+17trk7YO+xG9D2qSY6v9XVUS1OP1m8ee
wtv-client-address: 0.0.0.0
"""

# (sometimes) a aecond challenge is issued at login-stage-two
#wtv_challenge2 = "qHhCarnrMrLBTFqFMG333g3kVk58YGYT2ebkrmgz/rdG8/5Py90XGO3scSzHGe41X7dfJqXJ3qaoWQshHDnPmijr6wLAjj3jFd9FHi8ernz0Hy3L1AFq3PWX3HAABQrbwEi+8t1Ryh7y8dxDivgE1Q==";
#wtv_challenge_response2 = s.ProcessChallenge(wtv_challenge2)

print("Set incarnation to 2")

s.set_incarnation(2)

############## STEP 3: START RC4 STREAM

"""
200 OK
Connection: Keep-Alive
wtv-encrypted: true
wtv-client-time-zone: PST -0800
wtv-client-time-dst-rule: PST
wtv-client-date: Sun, 30 May 2021 23:13:47 GMT
wtv-country: US
wtv-language-header: en-US,en
wtv-visit: client:closeallpanels
wtv-expire-all: client:closeallpanels
wtv-ticket: 4p7Jzd+chEb4nfnHO3Xj8ctnB+YWim8KAqY381AGDoJQ77K9nxLWPE9pBumb6rBDkNiAz3IAfO570+F6isW/Ey3OQvzPHGa72FTYKZJweuM3JWVV5L6ILMPYuGb6A+q63PE3dUmPvAxM+onL5Ctr8XC01e43fiK0rihHdY9OWkMFmprf9PcXsHrkHnUT3UyVfZalg06YSsNoHYReHzb8jV0Cfbc1ocLEdCLgp89k5LIbOgM3fjbRCQJtcr705w0/sQ+gjISP4dlRcprJH83LQ/SO2PYzi48kLT+tTZS3AnjidKsBI+3r60sH/AK9+9XMbG1WOZeSKRkOBdgigu+ZPJXd86OOWNjiUxAFAeaKQyZx72V/lpqJ+tMNBf/qFonsKSxb5xkfgOunfwp8SCIkMUf/vjcpYH8tqdbkwXmVuRJukmoIQIzUOpQiDLmpR9uTJ5pndCDPCidpZv9uv2BKoaq8BUFKzV9aXs0eUBT9HN96euy4jG0cOp2Yx1Ts9EC1/WiK/tgONCW1ZktTRll/bha6ECgUWR/kd1dX7zNWyJEPpl0jCvsUyjuSaQjA40IFTDvZyjRzArOn0qrN8dBh+yuBIZMRWW2KDYKR4mFdlXTW+5RFRn4fCfoJh7fNjwlcjKbdyFZ1m/mDJmWdmUYLFXor6bIQvZHMwgVbI4wBeOGJBtnUB2Lksy5DOVFulWf6LQzoTeFK71G+yZBx/91uI03Q/WW2kAA3spVxf4ZpsU3+KByRWL2WDkVIWHf3pMwgV0XZU6u18vZxbzwLfjKFbywA/AK0xmmu8Hw25JsiEenKxbYccXsavI8cq0/hIWYC+afLaoepytReRixswxddmazH2JXT3IIh
wtv-noback-all: wtv-
wtv-service: name=wtv-register host=74.76.120.18 port=1607
wtv-visit: wtv-register:/register-wtv-token-1684386180-4337B19491C7FB61EB41D4C144B44273?ForceRegistration=true
wtv-phone-log-url: wtv-log:/phone-log
Content-length: 0
Content-type: text/html
"""
# The ticket stores the session keys for the server.  The client stores the initial key in NVRAM and session keys in memory

"""
SECURE ON
Accept-Language: en-US,en
wtv-ticket: 4p7Jzd+chEb4nfnHO3Xj8ctnB+YWim8KAqY381AGDoJQ77K9nxLWPE9pBumb6rBDkNiAz3IAfO570+F6isW/Ey3OQvzPHGa72FTYKZJweuM3JWVV5L6ILMPYuGb6A+q63PE3dUmPvAxM+onL5Ctr8XC01e43fiK0rihHdY9OWkMFmprf9PcXsHrkHnUT3UyVfZalg06YSsNoHYReHzb8jV0Cfbc1ocLEdCLgp89k5LIbOgM3fjbRCQJtcr705w0/sQ+gjISP4dlRcprJH83LQ/SO2PYzi48kLT+tTZS3AnjidKsBI+3r60sH/AK9+9XMbG1WOZeSKRkOBdgigu+ZPJXd86OOWNjiUxAFAeaKQyZx72V/lpqJ+tMNBf/qFonsKSxb5xkfgOunfwp8SCIkMUf/vjcpYH8tqdbkwXmVuRJukmoIQIzUOpQiDLmpR9uTJ5pndCDPCidpZv9uv2BKoaq8BUFKzV9aXs0eUBT9HN96euy4jG0cOp2Yx1Ts9EC1/WiK/tgONCW1ZktTRll/bha6ECgUWR/kd1dX7zNWyJEPpl0jCvsUyjuSaQjA40IFTDvZyjRzArOn0qrN8dBh+yuBIZMRWW2KDYKR4mFdlXTW+5RFRn4fCfoJh7fNjwlcjKbdyFZ1m/mDJmWdmUYLFXor6bIQvZHMwgVbI4wBeOGJBtnUB2Lksy5DOVFulWf6LQzoTeFK71G+yZBx/91uI03Q/WW2kAA3spVxf4ZpsU3+KByRWL2WDkVIWHf3pMwgV0XZU6u18vZxbzwLfjKFbywA/AK0xmmu8Hw25JsiEenKxbYccXsavI8cq0/hIWYC+afLaoepytReRixswxddmazH2JXT3IIh
wtv-connect-session-id: c84aa151
wtv-client-serial-number: n00b_for_life_01
wtv-system-version: 16276
wtv-capability-flags: 3C04F199BDDEFCF
wtv-client-bootrom-version: 2046
wtv-client-rom-type: US-LC2-disk-0MB-8MB
wtv-system-chipversion: 53608448
User-Agent: Mozilla/4.0 WebTV/2.8.2 (compatible; MSIE 4.0)
wtv-encryption: true
wtv-script-id: 0
wtv-script-mod: 0
wtv-incarnation:4
"""
# Client sends SECURE ON to start the RC4 stream

print("Set incarnation to 4")

s.set_incarnation(4)
s.SecureOn()

print("START RC4 STREAM")

############## STEP 4: SEND REQUESTS USING RC4

# Decrypting an RC4 stream is sequential.  You can't decrypt mid-stream it has to be decrypted in the order it went.
# Each time you open a connection you must setup the RC4 connection

encrypted_request = b'\x73\x32\x91\x6d\x0e\xaf\xaf\x1b\xdd\xda\x02\x60\xbe\x60\x3a\x58\x5e\xa2\xfd\x08\x8e\x6e\x1a\x2d\xc7\x7a\x26\xcb\x56\xab\x1b\x3b\xe7\xaa\x5a\x1f\xa6\xa6\x2c\x8f\x2d\xae\x85\x52\xc4\x9f\xe9\xec\x4b\x2b\xf6\x41\x09\x36\xba\x23\xba\x7c\x24\x5f\xe7\x6c\xaa\x8f\x8e\x1a\x07\x19\x1d\x4f\x86\xd5\xc7\xce\x02\x66\x21\x23\x8b\x21\x5b\x4d\xe9\x1b\xec\x27\x3a\x65\x9a\xab\x32\x75\x37\x1e\xbe\x5d\xcd\x61\xfc\x51\x27\x2b\x82\x38\xbe\xd0\x7c\xae\x23\x34\xb3\x6e\x0e\x97\xf3\xb7\xdc\x34\x86\x0f\xf1\x16\x42\x11\x09\x85\xb3\xf5\x57\xa8\x49\xb2\x34\xa4\xf8\x15\x51\xa7\x93\x94\x7e\x11\x05\x03\x14\xa6\xfc\x8d\x37\xfa\x4a\x38\x45\x9c\x64\x45\x25\x1a\x7a\x69\x91\x42\xf5\x75\xd6\x3f\x39\x47\x3a\x86\xf4\x95\xd7\x38\xe4\x3d\x6f\x76\xcf\x5d\xe7\xb3\xee\xe9\x70\xf2\xe3\x34\x20\x9d\xb3\x58\xab\x90\x95\xcc\x07\x13\xad\x24\x69\xa2\x57\xd8\x37\x8d\x1f\x5a\x91\x99\x7d\x86\x99\x4d\x6e\xb5\x5d\x9f\x35\x7d\x7a\xf5\xc6\x06\x92\x32\x1b\x9a\x16\xde\xf0\x21\xc6\xea\xd4\x24\x2d\xd2\x78\x7d\xaa\xea\x37\xf4\xd6\x8c\x93\x4b\xb4\xe1\x5e\x9e\xa6\x8f\xf3\x33\xee\x26\xa8\xab\xd9\x1d\xab\xff\x51\xd0\xfe\x4d\xe1\xb6\x68\x77\x84\x3b\x80\x6a\x11\x47\xec\x86\x48\x38\xd6\x08\x5e\x8b\xf3\xbe\xf6\xdf\xd2\xad\x73\x9a\x52\x8a\x41\x20\x9e\xe6\x4d\x4c\x49\xf3\x90\xc8\x43\x07\x61\xb3\xc9\x98\xd4\xa3\x1f\xe8\xfe\xac\xd8\xc6\xd9\x62\x49\x71\x81\xd3\x0b\x6c\x13\x77\xdc\x7a\xbd\x1e\x5b'
text_request = s.DecryptKey1(encrypted_request)
print(text_request)

encrypted_request2 = b'\xc9\x48\x57\xc4\xfa\x49\x49\xeb\xf1\xa0\x40\x01\xe2\xfd\x73\xb8\xc6\x3f\xcd\xb7\xe1\x21\x2a\xfa\x3d\xd8\x5f\xa8\x35\x53\x1f\x60\x17\x9d\x6c\x8f\x97\xd2\xa1\x96\x5e\x7a\x96\xe5\xf9\xf3\xee\x7a\x51\x89\x1c\x67\x50\x31\xe3\x05\x9e\x86\x11\xe2\xcd\x0c\x4b\x24\x69\xca\x6d\xc1\xe1\xdc\xc5\xf5\xdc\x12\xfc\x5c\xa5\xf2\xfd\x38\x8d\xe3\x21\xd0\x65\x18\xb2\xda\x4f\x37\x0b\xf0\x31\x16\xa0\x1b\x79\xae\x45\xa3\xe1\x7c\x0b\xdf\x43\x2d\x8f\xf3\x30\x0a\xcb\x4e\xf6\x8d\xca\x8b\x78\x67\x1c\x34\x6e\xc5\xfe\x78\xe2\x60\xd1\xe6\xa5\x73\x5e\x36\x8a\xd8\xcb\x53\x79\x93\xdb\x7a\x4b\x7d\x2f\x48\x17\x85\x0e\x37\xf1\xc4\xfc\x35\x55\x75\x35\xda\xbc\xe8\x2f\x51\x0e\xd8\xb5\xda\x4f\xad\x01\x44\x89\x37\x06\xc8\x63\xa8\xb9\x69\x5c\x81\x52\x1f\x82\xb4\x24\x9e\x72\xbb\x4b\xa0\xc1\x1e\xea\x76\x39\x56\xad\xcc\x44\xdd\x72\x19\x0e\xa8\xed\x1f\xec\x45\x97\xe6\x2c\xc0\xe7\x14\x9b\xc6\x24\x83\x36\x29\xb2\x6b\xad\x55\x49\x2d\x66\x66\x3e\xbc\xbf\xa4\xeb\x66\x0d\xb4\x92\xb9\xd1\x88\x5d\x18\x05\x1d\x17\x93\xd3\xd6\x79\x3a\xc7\x8e\x94\xf6\xf1\xd9\x88\xcd\xf6\x4a\x69\x8a\xa9\x2f\x0b\x2a\x15\x29\x04\x32\x8b\x5a\xbd\x99\xf2\x5c\x8b\x25\x11\x96\xee\x13\xc3\xd4\x35\x49\xcc\xa7\xcb\xf9\x24\xe3\x19\xc2\x73\x4f\x02\xd3\xe1\x1d\x2b\xea\xea\x32\x9b\x62\xbb\xf2\xcc\x71\x4f\xb5\xd2\x34\xe6\x90\x3d\xb3\x79\xd2\x38\xa1\xca\x8f\x94\xd3\x8c\x9c\x6d\x27\x4d\xe8\xb6\x75\xa2\x77\x6e\xef\xd8\xd2\xf2\x5d'
text_request2 = s.DecryptKey1(encrypted_request2)
print(text_request2)

encrypted_request3 = b'\xf9\x96\x1c\xd0\x81\x78\xf9\x12\x13\x03\xa7\xa2\x21\x47\x73\xb9\x47\x14\x66\xf3\x5b\x35\x28\xb6\x93\x6e\x25\xa5\xb4\x16\xe6\xe9\x00\xbf\x4e\x94\x92\x79\x67\x52\xb4\xa6\xa0\x72\xdc\x34\x76\xcc\xd0\x37\x9d\x18\x51\xbd\xc8\xde\x6d\x73\x68\x20\x81\x04\x4d\x38\x09\x71\x13\x81\x8c\xae\x45\xf3\x1d\x4e\xae\xca\xc4\x4a\x71\x3f\xb2\x8a\xf4\x4e\x00\x80\xb4\x98\x81\xe7\x36\x8d\x81\x53\x91\x63\x0e\x93\x29\x6f\x2a\xc2\x0d\xcc\xe5\xf8\xd1\xe7\x24\xe8\x20\x30\x00\x3b\xfe\x6f\xa8\x42\x16\xfc\x53\xdf\xf7\x17\x96\x7c\x4e\x8e\xf1\xc1\x61\xae\x9f\xfe\x15\x91\x9e\xb8\xae\x52\x12\x4b\x4c\x18\xcb\x25\x3c\x06\x98\xf1\x22\xe9\x79\xc7\xf5\x68\x6b\xa2\x1f\x80\xae\x8b\xfe\xa2\x76\x3d\x22\x3a\x86\xd8\x05\x1c\x4d\xdd\xd5\x57\x50\xed\xcf\xc9\x6e\x78\x89\xfb\x31\x24\x42\xb5\x11\x49\xca\xcd\xa1\x4c\x2c\x99\xf2\xc6\xca\x74\x92\xee\xf1\x38\xe2\x7f\x39\xc8\x65\xbf\xea\xb3\x0f\x6d\x63\x2d\x6c\xff\x10\x68\x9a\x69\x0e\x79\x32\x6b\x6c\x29\xeb\x7c\x05\x64\xe6\x92\x51\x9f\x5a\x74\x02\x56\xd3\x60\xc8\x9b\xc5\x94\xec\xc0\xbc\x9e\xb7\x71\x5b\x42\x46\xdf'
text_request3 = s.DecryptKey1(encrypted_request3)
print(text_request3)

####

"""
SECURE ON
Accept-Language: en-US,en
wtv-ticket: 4p7Jzd+chEb4nfnHO3Xj8ctnB+YWim8KAqY381AGDoJQ77K9nxLWPE9pBumb6rBDkNiAz3IAfO570+F6isW/Ey3OQvzPHGa72FTYKZJweuM3JWVV5L6ILMPYuGb6A+q63PE3dUmPvAxM+onL5Ctr8XC01e43fiK0rihHdY9OWkMFmprf9PcXsHrkHnUT3UyVfZalg06YSsNoHYReHzb8jV0Cfbc1ocLEdCLgp89k5LIbOgM3fjbRCQJtcr705w0/sQ+gjISP4dlRcprJH83LQ/SO2PYzi48kLT+tTZS3AnjidKsBI+3r60sH/AK9+9XMbG1WOZeSKRkOBdgigu+ZPJXd86OOWNjiUxAFAeaKQyZx72V/lpqJ+tMNBf/qFonsKSxb5xkfgOunfwp8SCIkMUf/vjcpYH8tqdbkwXmVuRJukmoIQIzUOpQiDLmpR9uTJ5pndCDPCidpZv9uv2BKoaq8BUFKzV9aXs0eUBT9HN96euy4jG0cOp2Yx1Ts9EC1/WiK/tgONCW1ZktTRll/bha6ECgUWR/kd1dX7zNWyJEPpl0jCvsUyjuSaQjA40IFTDvZyjRzArOn0qrN8dBh+yuBIZMRWW2KDYKR4mFdlXTW+5RFRn4fCfoJh7fNjwlcjKbdyFZ1m/mDJmWdmUYLFXor6bIQvZHMwgVbI4wBeOGJBtnUB2Lksy5DOVFulWf6LQzoTeFK71G+yZBx/91uI03Q/WW2kAA3spVxf4ZpsU3+KByRWL2WDkVIWHf3pMwgV0XZU6u18vZxbzwLfjKFbywA/AK0xmmu8Hw25JsiEenKxbYccXsavI8cq0/hIWYC+afLaoepytReRixswxddmazH2JXT3IIh
wtv-connect-session-id: c84aa151
wtv-client-serial-number: n00b_for_life_01
wtv-system-version: 16276
wtv-capability-flags: 3C04F199BDDEFCF
wtv-client-bootrom-version: 2046
wtv-client-rom-type: US-LC2-disk-0MB-8MB
wtv-system-chipversion: 53608448
User-Agent: Mozilla/4.0 WebTV/2.8.2 (compatible; MSIE 4.0)
wtv-encryption: true
wtv-script-id: 0
wtv-script-mod: 0
wtv-incarnation:6
"""

s.set_incarnation(6)
s.SecureOn()

encrypted_request4 = b'\x3b\x43\x6b\x16\xb2\x71\x5b\x37\xab\xc8\x11\xa2\xa2\x86\x59\x49\xda\x5a\x7c\xcf\x37\x6c\x1c\x74\x9d\x6a\xba\x6d\xce\x53\xeb\x2d\xb6\xd1\x4d\x00\xea\xc4\x5d\xe6\x64\x61\x16\xec\x2c\xeb\xea\x54\xf2\xf1\x07\x7d\x94\x4e\x39\xd5\xda\x8a\x05\x1f\xfe\xa6\x1c\x68\xd1\x43\x11\x6e\xe8\x70\xa9\x1a\x79\x01\x9a\x01\x91\x40\x22\x16\xf4\x86\x29\x74\x89\x4b\x61\xec\x39\x09\xda\xb8\xd2\x3e\x99\x79\x95\x15\xd2\xd5\x26\x33\x8e\xcb\x5c\x7d\x76\x39\xfb\x08\xdc\x5b\xd7\xa9\xa9\x62\x41\x52\xd6\xec\x00\x06\x3e\xc1\x35\xfb\xb5\xc1\xf6\xb1\x6d\x0b\xc9\x8d\x48\xbf\x0f\x30\x08\xbe\x13\x44\x3e\x20\xc5\x82\xb5\xf6\xce\x7b\x39\x88\xfc\x3c\x60\xe8\xe4\xb5\x42\xf2\x5b\x85\xe1\x08\x06\x31\x76\xde\xb1\x73\x79\x76\x66\x41\x80\xe9\x7e\x88\x52\xdb\xf6\xa2\x6f\x47\x6c\x2a\xcb\xb8\xfb\x98\x14\x1e\x15\x9f\xd8\xe4\x6f\x21\xbf\xa9\x50\x8b\x24\xf2\x03\x00\x3c\xb3\xc3\xb1\x0a\x66\x4e\x79\xc3\x7e\xae\xf4\xb2\xfa\xe3\x2b\x58\xef\x0f\x13\x53\xbc\x7b\x17\xb7\x10\x75\xaa\x65\x37\x11\x95\x13\x64\x0e\x14\xe5\x33\x42\x7e\x6a\xe5\xff\xea\xc0\xd7'
text_request4 = s.DecryptKey1(encrypted_request4)
print(text_request4)
