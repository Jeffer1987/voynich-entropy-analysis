import random
from typing import List, Set, Union, Optional

TABLES = {
    'a': {
        'A': {'unigram': '<ol>', 'bigram_start': '<sh>', 'bigram_end': '<aiin>'},
        'B': {'unigram': '<qokchdy>', 'bigram_start': '<dol>', 'bigram_end': '<l>'},
        'C': {'unigram': '<chey>', 'bigram_start': '<lch>', 'bigram_end': '<eeey>'},
        'D': {'unigram': '<cheey>', 'bigram_start': '<o>', 'bigram_end': '<eeody>'},
        'E': {'unigram': '<chedy>', 'bigram_start': '<ch>', 'bigram_end': '<edy>'},
        'F': {'unigram': '<qokchey>', 'bigram_start': '<shckh>', 'bigram_end': '<eam>'},
        'G': {'unigram': '<qokchy>', 'bigram_start': '<cph>', 'bigram_end': '<g>'},
        'H': {'unigram': '<qokchedy>', 'bigram_start': '<qotch>', 'bigram_end': '<eedal>'},
        'I': {'unigram': '<shedy>', 'bigram_start': '<k>', 'bigram_end': '<dy>'},
        'L': {'unigram': '<qokal>', 'bigram_start': '<cth>', 'bigram_end': '<es>'},
        'M': {'unigram': '<qokar>', 'bigram_start': '<l>', 'bigram_end': '<ody>'},
        'N': {'unigram': '<daiin>', 'bigram_start': '<opch>', 'bigram_end': '<al>'},
        'O': {'unigram': '<aiin>', 'bigram_start': '<r>', 'bigram_end': '<or>'},
        'P': {'unigram': '<qoky>', 'bigram_start': '<dch>', 'bigram_end': '<edar>'},
        'Q': {'unigram': '<qokol>', 'bigram_start': '<dl>', 'bigram_end': '<iin>'},
        'R': {'unigram': '<qokeedy>', 'bigram_start': '<t>', 'bigram_end': '<eedy>'},
        'S': {'unigram': '<qokeey>', 'bigram_start': '<lk>', 'bigram_end': '<ar>'},
        'T': {'unigram': '<qokaiin>', 'bigram_start': '<qok>', 'bigram_end': '<y>'},
        'U': {'unigram': '<qokain>', 'bigram_start': '<ot>', 'bigram_end': '<eey>'},
        'V': {'unigram': '<qokey>', 'bigram_start': '<qockh>', 'bigram_end': '<edor>'},
        'X': {'unigram': '<qokor>', 'bigram_start': '<lpch>', 'bigram_end': '<edo>'},
        'Y': {'unigram': '<qokdy>', 'bigram_start': '<ry>', 'bigram_end': '<oin>'},
        'Z': {'unigram': '<qokeeedy>', 'bigram_start': '<ols>', 'bigram_end': '<eeaiin>'},
    },
    'b1': {
        'A': {'unigram': '<or>', 'bigram_start': '<yt>', 'bigram_end': '<eol>'},
        'B': {'unigram': '<okchdy>', 'bigram_start': '<qolch>', 'bigram_end': '<ory>'},
        'C': {'unigram': '<okedy>', 'bigram_start': '<tsh>', 'bigram_end': '<r>'},
        'D': {'unigram': '<cheedy>', 'bigram_start': '<dal>', 'bigram_end': '<eeos>'},
        'E': {'unigram': '<ar>', 'bigram_start': '<ok>', 'bigram_end': '<ey>'},
        'F': {'unigram': '<okchey>', 'bigram_start': '<rsh>', 'bigram_end': '<iiin>'},
        'G': {'unigram': '<okchy>', 'bigram_start': '<solch>', 'bigram_end': '<eols>'},
        'H': {'unigram': '<okchedy>', 'bigram_start': '<oiin>', 'bigram_end': '<er>'},
        'I': {'unigram': '<qokedy>', 'bigram_start': '<yk>', 'bigram_end': '<eody>'},
        'L': {'unigram': '<okal>', 'bigram_start': '<ypch>', 'bigram_end': '<eedaiin>'},
        'M': {'unigram': '<okar>', 'bigram_start': '<s>', 'bigram_end': '<edain>'},
        'N': {'unigram': '<dal>', 'bigram_start': '<kch>', 'bigram_end': '<d>'},
        'O': {'unigram': '<al>', 'bigram_start': '<lkch>', 'bigram_end': '<eos>'},
        'P': {'unigram': '<oky>', 'bigram_start': '<qoksh>', 'bigram_end': '<as>'},
        'Q': {'unigram': '<okol>', 'bigram_start': '<of>', 'bigram_end': '<als>'},
        'R': {'unigram': '<okeedy>', 'bigram_start': '<tch>', 'bigram_end': '<daiin>'},
        'S': {'unigram': '<okeey>', 'bigram_start': '<or>', 'bigram_end': '<eeo>'},
        'T': {'unigram': '<okaiin>', 'bigram_start': '<pch>', 'bigram_end': '<am>'},
        'U': {'unigram': '<okain>', 'bigram_start': '<olk>', 'bigram_end': '<eo>'},
        'V': {'unigram': '<okey>', 'bigram_start': '<daly>', 'bigram_end': '<sy>'},
        'X': {'unigram': '<okor>', 'bigram_start': '<f>', 'bigram_end': '<eeeos>'},
        'Y': {'unigram': '<okdy>', 'bigram_start': '<sok>', 'bigram_end': '<eory>'},
        'Z': {'unigram': '<okeeedy>', 'bigram_start': '<lfch>', 'bigram_end': '<eds>'},
    },
    'b2': {
        'A': {'unigram': '<qol>', 'bigram_start': '<olch>', 'bigram_end': '<air>'},
        'B': {'unigram': '<otchdy>', 'bigram_start': '<dor>', 'bigram_end': '<oy>'},
        'C': {'unigram': '<lkaiin>', 'bigram_start': '<y>', 'bigram_end': '<aiiin>'},
        'D': {'unigram': '<lkain>', 'bigram_start': '<otsh>', 'bigram_end': '<dol>'},
        'E': {'unigram': '<dar>', 'bigram_start': '<ol>', 'bigram_end': '<ol>'},
        'F': {'unigram': '<otchey>', 'bigram_start': '<ly>', 'bigram_end': '<daiiin>'},
        'G': {'unigram': '<otchy>', 'bigram_start': '<ssh>', 'bigram_end': '<saiin>'},
        'H': {'unigram': '<otchedy>', 'bigram_start': '<aly>', 'bigram_end': '<eaiin>'},
        'I': {'unigram': '<shey>', 'bigram_start': '<qot>', 'bigram_end': '<eor>'},
        'L': {'unigram': '<otal>', 'bigram_start': '<sch>', 'bigram_end': '<edol>'},
        'M': {'unigram': '<otar>', 'bigram_start': '<shcth>', 'bigram_end': '<dain>'},
        'N': {'unigram': '<dain>', 'bigram_start': '<okch>', 'bigram_end': '<oiin>'},
        'O': {'unigram': '<ain>', 'bigram_start': '<lt>', 'bigram_end': '<eeedy>'},
        'P': {'unigram': '<oty>', 'bigram_start': '<qolk>', 'bigram_end': '<eeod>'},
        'Q': {'unigram': '<otol>', 'bigram_start': '<dary>', 'bigram_end': '<edaiiin>'},
        'R': {'unigram': '<oteedy>', 'bigram_start': '<qopch>', 'bigram_end': '<s>'},
        'S': {'unigram': '<oteey>', 'bigram_start': '<sol>', 'bigram_end': '<edal>'},
        'T': {'unigram': '<otaiin>', 'bigram_start': '<od>', 'bigram_end': '<edaiin>'},
        'U': {'unigram': '<otain>', 'bigram_start': '<p>', 'bigram_end': '<eeol>'},
        'V': {'unigram': '<otey>', 'bigram_start': '<sar>', 'bigram_end': '<sdy>'},
        'X': {'unigram': '<otor>', 'bigram_start': '<do>', 'bigram_end': '<ery>'},
        'Y': {'unigram': '<otdy>', 'bigram_start': '<olpch>', 'bigram_end': '<osy>'},
        'Z': {'unigram': '<oteeedy>', 'bigram_start': '<om>', 'bigram_end': '<eda>'},
    },
    'b3': {
        'A': {'unigram': '<chdy>', 'bigram_start': '<ls>', 'bigram_end': '<ed>'},
        'B': {'unigram': '<sheckhy>', 'bigram_start': '<octh>', 'bigram_end': '<eoy>'},
        'C': {'unigram': '<shckhy>', 'bigram_start': '<och>', 'bigram_end': '<aiir>'},
        'D': {'unigram': '<chor>', 'bigram_start': '<dar>', 'bigram_end': '<oly>'},
        'E': {'unigram': '<dar>', 'bigram_start': '<qo>', 'bigram_end': '<ain>'},
        'F': {'unigram': '<shal>', 'bigram_start': '<osh>', 'bigram_end': '<do>'},
        'G': {'unigram': '<shar>', 'bigram_start': '<orch>', 'bigram_end': '<eeam>'},
        'H': {'unigram': '<shy>', 'bigram_start': '<qoch>', 'bigram_end': '<eeoy>'},
        'I': {'unigram': '<otedy>', 'bigram_start': '<ych>', 'bigram_end': '<o>'},
        'L': {'unigram': '<saiin>', 'bigram_start': '<ykch>', 'bigram_end': '<edair>'},
        'M': {'unigram': '<sain>', 'bigram_start': '<aiiin>', 'bigram_end': '<eedar>'},
        'N': {'unigram': '<dy>', 'bigram_start': '<oly>', 'bigram_end': '<eod>'},
        'O': {'unigram': '<y>', 'bigram_start': '<ody>', 'bigram_end': '<edam>'},
        'P': {'unigram': '<sheody>', 'bigram_start': '<ofch>', 'bigram_end': '<e>'},
        'Q': {'unigram': '<shody>', 'bigram_start': '<es>', 'bigram_end': '<ols>'},
        'R': {'unigram': '<sheol>', 'bigram_start': '<ysh>', 'bigram_end': '<eeor>'},
        'S': {'unigram': '<shol>', 'bigram_start': '<chcth>', 'bigram_end': '<eed>'},
        'T': {'unigram': '<sheey>', 'bigram_start': '<ar>', 'bigram_end': '<ees>'},
        'U': {'unigram': '<sheedy>', 'bigram_start': '<op>', 'bigram_end': '<eal>'},
        'V': {'unigram': '<shor>', 'bigram_start': '<dyk>', 'bigram_end': '<sd>'},
        'X': {'unigram': '<shaiin>', 'bigram_start': '<qolsh>', 'bigram_end': '<ch>'},
        'Y': {'unigram': '<shain>', 'bigram_start': '<opsh>', 'bigram_end': '<yl>'},
        'Z': {'unigram': '<sheeey>', 'bigram_start': '<daiir>', 'bigram_end': '<ady>'},
    },
    'c1': {
        'A': {'unigram': '<chol>', 'bigram_start': '<chckh>', 'bigram_end': '<dal>'},
        'B': {'unigram': '<qotchdy>', 'bigram_start': '<psh>', 'bigram_end': '<eeed>'},
        'C': {'unigram': '<sar>', 'bigram_start': '<qofch>', 'bigram_end': '<ail>'},
        'D': {'unigram': '<chckhey>', 'bigram_start': '<qol>', 'bigram_end': '<eeeody>'},
        'E': {'unigram': '<chckhy>', 'bigram_start': '<dsh>', 'bigram_end': '<ear>'},
        'F': {'unigram': '<qotchey>', 'bigram_start': '<qotsh>', 'bigram_end': '<eel>'},
        'G': {'unigram': '<qotchy>', 'bigram_start': '<sy>', 'bigram_end': '<ok>'},
        'H': {'unigram': '<qotchedy>', 'bigram_start': '<ory>', 'bigram_end': '<eedam>'},
        'I': {'unigram': '<raiin>', 'bigram_start': '<sal>', 'bigram_end': '<od>'},
        'L': {'unigram': '<qotal>', 'bigram_start': '<qokch>', 'bigram_end': '<daly>'},
        'M': {'unigram': '<qotar>', 'bigram_start': '<q>', 'bigram_end': '<dor>'},
        'N': {'unigram': '<dair>', 'bigram_start': '<aiir>', 'bigram_end': '<eees>'},
        'O': {'unigram': '<air>', 'bigram_start': '<solk>', 'bigram_end': '<dair>'},
        'P': {'unigram': '<qoty>', 'bigram_start': '<qor>', 'bigram_end': '<eoly>'},
        'Q': {'unigram': '<qotol>', 'bigram_start': '<air>', 'bigram_end': '<ealy>'},
        'R': {'unigram': '<qoteedy>', 'bigram_start': '<qop>', 'bigram_end': '<dam>'},
        'S': {'unigram': '<qoteey>', 'bigram_start': '<ytch>', 'bigram_end': '<an>'},
        'T': {'unigram': '<qotaiin>', 'bigram_start': '<rch>', 'bigram_end': '<ary>'},
        'U': {'unigram': '<qotain>', 'bigram_start': '<ckh>', 'bigram_end': '<ee>'},
        'V': {'unigram': '<qotey>', 'bigram_start': '<da>', 'bigram_end': '<aiis>'},
        'X': {'unigram': '<qotor>', 'bigram_start': '<dk>', 'bigram_end': '<dl>'},
        'Y': {'unigram': '<qotdy>', 'bigram_start': '<sk>', 'bigram_end': '<ry>'},
        'Z': {'unigram': '<qoteeedy>', 'bigram_start': '<so>', 'bigram_end': '<in>'},
    },
    'c2': {
        'A': {'unigram': '<cheol>', 'bigram_start': '<al>', 'bigram_end': '<aly>'},
        'B': {'unigram': '<olkchdy>', 'bigram_start': '<ary>', 'bigram_end': '<eom>'},
        'C': {'unigram': '<lchey>', 'bigram_start': '<olt>', 'bigram_end': '<esy>'},
        'D': {'unigram': '<olkedy>', 'bigram_start': '<sair>', 'bigram_end': '<a>'},
        'E': {'unigram': '<lchedy>', 'bigram_start': '<lsh>', 'bigram_end': '<dar>'},
        'F': {'unigram': '<olkchey>', 'bigram_start': '<dair>', 'bigram_end': '<sairy>'},
        'G': {'unigram': '<olkchy>', 'bigram_start': '<dyt>', 'bigram_end': '<iir>'},
        'H': {'unigram': '<olkchedy>', 'bigram_start': '<qocth>', 'bigram_end': '<eer>'},
        'I': {'unigram': '<qotedy>', 'bigram_start': '<olsh>', 'bigram_end': '<m>'},
        'L': {'unigram': '<olkal>', 'bigram_start': '<ockh>', 'bigram_end': '<eesy>'},
        'M': {'unigram': '<olkar>', 'bigram_start': '<d>', 'bigram_end': '<eeal>'},
        'N': {'unigram': '<dam>', 'bigram_start': '<os>', 'bigram_end': '<eain>'},
        'O': {'unigram': '<am>', 'bigram_start': '<oksh>', 'bigram_end': '<aim>'},
        'P': {'unigram': '<olky>', 'bigram_start': '<chcph>', 'bigram_end': '<ais>'},
        'Q': {'unigram': '<olkol>', 'bigram_start': '<oiiin>', 'bigram_end': '<oiiin>'},
        'R': {'unigram': '<olkeedy>', 'bigram_start': '<otch>', 'bigram_end': '<eear>'},
        'S': {'unigram': '<olkeey>', 'bigram_start': '<ksh>', 'bigram_end': '<os>'},
        'T': {'unigram': '<olkaiin>', 'bigram_start': '<sor>', 'bigram_end': '<om>'},
        'U': {'unigram': '<olkain>', 'bigram_start': '<fch>', 'bigram_end': '<eedain>'},
        'V': {'unigram': '<olkey>', 'bigram_start': '<soiin>', 'bigram_end': '<eeeo>'},
        'X': {'unigram': '<olkor>', 'bigram_start': '<x>', 'bigram_end': '<eedo>'},
        'Y': {'unigram': '<olkdy>', 'bigram_start': '<ail>', 'bigram_end': '<yr>'},
        'Z': {'unigram': '<olkeeedy>', 'bigram_start': '<chcfh>', 'bigram_end': '<alsy>'},
    },
}

class NaibbeEncoder:
    """
    Replication of the Naibbe Encoder.
    
    This encoder translates plaintexts into ciphertexts resembling the Voynich 
    graphemes based on positional rules, card drawing (selecting cipher tables),
    and specific letter conversions.
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the encoder.
        
        Args:
            seed: Optional seed for the random number generator.
        """
        self.seed = seed
        self.rng = random.Random(seed)
        self.deck: List[str] = []
        self.reset_deck()
        
        # Build the set of clean unigram word types for the ambiguity check
        self.unigram_word_types: Set[str] = set()
        for tbl in TABLES.values():
            for letter_entry in tbl.values():
                uni = letter_entry['unigram']
                if uni:
                    # Strip brackets for exact matches during concatenation checks
                    clean_uni = uni.replace('<', '').replace('>', '').strip()
                    self.unigram_word_types.add(clean_uni)
                    
    def reset_deck(self) -> None:
        """Resets and shuffles the table deck."""
        # Card table weighting: a (20), b1 (8), b2 (8), b3 (8), c1 (4), c2 (4)
        self.deck = ['a']*20 + ['b1']*8 + ['b2']*8 + ['b3']*8 + ['c1']*4 + ['c2']*4
        self.rng.shuffle(self.deck)
        
    def draw_card(self) -> str:
        """Draws a card from the deck. Reinitializes and shuffles if empty."""
        if not self.deck:
            self.reset_deck()
        return self.deck.pop(0)
        
    def normalize(self, text: str) -> str:
        """
        Normalizes plaintext to a 23-letter alphabet compatible with the encoder.
        - Converts to lowercase.
        - Translates J -> I, W -> U.
        - Keeps only the alphabet: 'abcdefghilmnopqrstuvxyz'.
        
        Args:
            text: The plaintext string.
            
        Returns:
            Normalized lowercase string.
        """
        text = text.lower()
        text = text.replace('j', 'i').replace('w', 'u')
        alphabet = set("abcdefghilmnopqrstuvxyz")
        cleaned = [c for c in text if c in alphabet]
        return "".join(cleaned)
        
    def respace(self, text: str) -> List[str]:
        """
        Segments text randomly into unigrams and bigrams based on simulated 
        dice rolls, mirroring historical/manual spacing variations.
        
        Args:
            text: Normalized plaintext string.
            
        Returns:
            A list of 1-character or 2-character tokens.
        """
        segments = []
        i = 0
        while i < len(text):
            if i == len(text) - 1:
                segments.append(text[i])
                i += 1
            else:
                d1 = self.rng.randint(1, 6)
                d2 = self.rng.randint(1, 6)
                # Snake eyes: d1=1, d2=1
                # Standard respacing: odd leftmost die (except snake eyes) -> space after 1 char
                if d1 % 2 == 1 and not (d1 == 1 and d2 == 1):
                    segments.append(text[i])
                    i += 1
                else:
                    segments.append(text[i:i+2])
                    i += 2
        return segments
        
    def encrypt_token(self, token: str, unambiguous: bool = True) -> str:
        """
        Encrypts a single token (unigram or bigram) into the Voynich EVA representation.
        
        Args:
            token: A string of length 1 or 2.
            unambiguous: If True, rejects bigram encodings that clash with unigram words.
            
        Returns:
            Encrypted token wrapped in EVA brackets (e.g. '<ol>').
        """
        if len(token) == 1:
            # unigram
            letter = token.upper()
            tbl = self.draw_card()
            val = TABLES[tbl][letter]['unigram']
            return val
        else:
            # bigram
            l1, l2 = token[0].upper(), token[1].upper()
            while True:
                tbl1 = self.draw_card()
                tbl2 = self.draw_card()
                prefix = TABLES[tbl1][l1]['bigram_start'].replace('<', '').replace('>', '').strip()
                suffix = TABLES[tbl2][l2]['bigram_end'].replace('<', '').replace('>', '').strip()
                enc_val = f"{prefix}{suffix}"
                
                if unambiguous and enc_val in self.unigram_word_types:
                    # Ambiguous, reject and redraw cards
                    continue
                
                return f"<{enc_val}>"
                
    def encode(self, plaintext: str, unambiguous: bool = True) -> str:
        """
        Encodes a plaintext document.
        
        Args:
            plaintext: Raw input text.
            unambiguous: Whether to prevent bigram/unigram clashes.
            
        Returns:
            The ciphertext string of space-separated EVA tokens.
        """
        normalized = self.normalize(plaintext)
        segments = self.respace(normalized)
        cipher_tokens = []
        for seg in segments:
            cipher_tokens.append(self.encrypt_token(seg, unambiguous=unambiguous))
        return " ".join(cipher_tokens)
