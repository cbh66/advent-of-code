type Length<T extends unknown[]> =
  T extends { length: infer L } ? L : number;

type Chars<S extends string> = 
  S extends `${infer A}${infer B}${infer C}${infer D}${infer E}${infer F}${infer Rest}`
    ? A | B | C | D | E | F | Chars<Rest>
    : S extends `${infer A}${infer B}${infer C}${infer D}${infer Rest}`
      ? A | B | C | D | Chars<Rest>
      : S extends `${infer A}${infer B}${infer Rest}`
        ? A | B | Chars<Rest>
        : S extends `${infer A}${infer Rest}`
          ? A | Chars<Rest>
          : never;

type InCommon<A extends string, B extends string, C extends string> =
  Chars<A> & Chars<B> & Chars<C>;

type Badges<L extends string[]> =
  L extends [
    infer A extends string, infer B extends string, infer C extends string,
    infer D extends string, infer E extends string, infer F extends string,
    infer G extends string, infer H extends string, infer I extends string,
    infer J extends string, infer K extends string, infer L extends string,
    ...(infer Rest extends string[])]
    ? [InCommon<A, B, C>, InCommon<D, E, F>, InCommon<G, H, I>, InCommon<J, K, L>, ...Badges<Rest>]
    : 
    L extends [
      infer A extends string, infer B extends string, infer C extends string,
      infer D extends string, infer E extends string, infer F extends string,
      ...(infer Rest extends string[])]
      ? [InCommon<A, B, C>, InCommon<D, E, F>, ...Badges<Rest>]
      : L extends [
        infer A extends string, infer B extends string, infer C extends string,
        ...(infer Rest extends string[])]
        ? [InCommon<A, B, C>, ...Badges<Rest>]
        : [];

interface LowerScores {
  a: [1];
  b: [1, 1];
  c: [1, 1, 1];
  d: [1, 1, 1, 1];
  e: [1, 1, 1, 1, 1];
  f: [1, 1, 1, 1, 1, 1];
  g: [1, 1, 1, 1, 1, 1, 1];
  h: [...LowerScores['g'], 1];
  i: [...LowerScores['g'], 1, 1];
  j: [...LowerScores['g'], 1, 1, 1];
  k: [...LowerScores['g'], 1, 1, 1, 1];
  l: [...LowerScores['g'], 1, 1, 1, 1, 1];
  m: [...LowerScores['g'], 1, 1, 1, 1, 1, 1];
  n: [...LowerScores['m'], 1];
  o: [...LowerScores['m'], 1, 1];
  p: [...LowerScores['m'], 1, 1, 1];
  q: [...LowerScores['m'], 1, 1, 1, 1];
  r: [...LowerScores['m'], 1, 1, 1, 1, 1];
  s: [...LowerScores['m'], 1, 1, 1, 1, 1, 1];
  t: [...LowerScores['s'], 1];
  u: [...LowerScores['s'], 1, 1];
  v: [...LowerScores['s'], 1, 1, 1];
  w: [...LowerScores['s'], 1, 1, 1, 1];
  x: [...LowerScores['s'], 1, 1, 1, 1, 1];
  y: [...LowerScores['s'], 1, 1, 1, 1, 1, 1];
  z: [...LowerScores['s'], 1, 1, 1, 1, 1, 1, 1];
}

type UpperScores = {
  [k in keyof LowerScores as Uppercase<k>]: [...LowerScores['z'], ...LowerScores[k]];
}

type Scores = LowerScores & UpperScores;

type Result<B extends string[]> =
  B extends [
    infer A extends keyof Scores,
    infer B extends keyof Scores,
    infer C extends keyof Scores,
    infer D extends keyof Scores,
    infer E extends keyof Scores,
    infer F extends keyof Scores,
    ...(infer Rest extends string[])]
    ? [...Scores[A], ...Scores[B], ...Scores[C],
      ...Scores[D], ...Scores[E], ...Scores[F], ...Result<Rest>]
    : B extends [
      infer A extends keyof Scores,
      infer B extends keyof Scores,
      infer C extends keyof Scores,
      infer D extends keyof Scores,
      ...(infer Rest extends string[])]
      ? [...Scores[A], ...Scores[B], ...Scores[C], ...Scores[D], ...Result<Rest>]
      : B extends [infer A extends keyof Scores, infer B extends keyof Scores,
        ...(infer Rest extends string[])]
        ? [...Scores[A], ...Scores[B], ...Result<Rest>]
        : B extends [infer A extends keyof Scores, ...(infer Rest extends string[])]
          ? [...Scores[A], ...Result<Rest>]
          : [];

type ExInput = [
"vJrwpWtwJgWrhcsFMMfFFhFp",
"jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
"PmmdzqPrVvPwwTWBwg",
"wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
"ttgJtRGJQctTZtZT",
"CrZsJsPPZsGzwwsLwLmpwMDw",
];

let exResult: Length<Result<Badges<ExInput>>>;

type FullInput = [
'mjpsHcssDzLTzMsz',
'tFhbtClRVtbhRCGBFntNTrLhqrwqWMDMTWTqMq',
'LltbngLGRSBgSgGRCJdSdQHvdfmQccmjSQ',
'lBslsZDDWdGdGpSMts',
'grQhDvqLQHDNGJJtbRMQQJ',
'HChCTnnLCgCrTZPPFzzVPcVD',
'ShrzjhNGrNqrhWnHHfVHbhnHbbhH',
'RBsvcBcDCdsRTsvgCgcPFRQpVQGQJPVFbnJfbJ',
'DvsTsdlCBsGLrjzmlqqz',
'WJJqZTgCnBLGCZBJCJnTLggTDDSDDMNdDSdbdSSsWDFfMsFf',
'PVjqpVHmPpvmcjhrRprFmQQffbfNbQMMsSMQNQ',
'cwcpRvrVlVgwtBwZqBzZ',
'qfJJmpqpmhsggvvpVPZCrhdFLFzZFDdLLh',
'CtCTBctGcGLSzZddGZSW',
'RlNjBCnjttBHHMMcQHCsRfsbfwgggmmJvmgfpm',
'ZmcgBBZhZMsnqnCPjpHPjLHp',
'dGbNwNtlTMTzGfNvTvdwNGVLPpQHPjLQPCpCjPqjLbpLPR',
'dvDTdfvNBhDZMBDZ',
'cvvRvbqcllbBVlvVVbVVlbVDjRjDjdMsHPZPGdDPGPHrDP',
'FwtpfwJtWwNtTTNnwFCtjDJsQdQPPPPMrjrPJHjH',
'CwFpnppgntShgbsscbms',
'cWMFMQpFNcvNDdBDgdsT',
'MPrrfrCHBBsDZCBJ',
'LmLjMLjjLWpVcRVR',
'ZrRZqlZMqTWrMDqwvnvVtnsvddvVnlVf',
'pQNhhLNNGmLjhhcfvndDpffdfdVf',
'QGjCLCQGmNgPBQDFFgTMJWWwMRTrTZWWBWTr',
'WrZWZPHHWZHprZVmVvqddBttBBhGhtvh',
'gzDlMTJDMfqhBGllhl',
'jJLqMMDDbbqjLpPHcsHLWZspPr',
'bsSVRVGsrDstrrSjcQjcjlPwzjQl',
'gHBggFNTTvTgfqgCFzljWwLWQQQnrwQWnf',
'NvJHgpgHvqBhNBJhHTvpBCJCZmtdpDsGsZdZMZRbVbbMdrZs',
'MPPtPwPnRnMPPnwrtNSGgLSCGGGNSLtSgD',
'hBhWFjfCsTbbbWqFFWBBqBhsWZVGSVglZHLSVDlNWDNHHGgV',
'zsCfTsTCMdmRPwzQ',
'JVQVvvszzvTsVsVJjctppcCtjtPRcTlP',
'MdFgqSddMqMDbtDlNjRDSR',
'qFZWZqwHlZfZvzvZfLZn',
'vpqwQSsHSHDQzDpgzwZlRLRZRRZTnTrrvGhh',
'JBcdmbmFMPgPbgfrZRZnRFFnrnLRln',
'JNdBNgbdJmPMWSSDzwVDtwSWWW',
'BDMcDDppHCStpWcHBDNtzPJjqGlllPMJzPGjwjlq',
'CZdZLmgCdqbPzjblZj',
'vndLfnghRQmVrhdvgBHpSCDWHBBCVHNppD',
'WrhrJJGSWzpTWwts',
'VlLPmqgmRNZRGwsvttjgcwsT',
'PDZmlbdVqLmPlddVNRDmmmbbSFHrCFQCnFBFJHSJGrDQCBrr',
'hvPdpvhHvHvPrNfVhDfjggFfRV',
'zlGwJGslsSDRfjsg',
'MJMWjMJzwqWGzJwMqJBTCmHndPPdCBvmdCpmHn',
'PVWFpQhJhFJpGbRCvRHGCp',
'jgslDjftsqhNglTgllgTqMnlHwCcvwZwRccSRCbGSGbCMHRw',
'TgjhNNnjlTfjTdDqTfhjnmzmWPzWrLdrQBPJFWJWBB',
'qPPRMPlfSzSSSPPnnLnqMlpQQtrrtmWpbFtQrdzrtrWt',
'BBvCcwsVThsBgswDBCFQHQpdmQvtrFpWFvWp',
'gCghTJgVCgDGVMlRGMqZnSWqlM',
'RWbHvrbHBsbWBHJWvJwMtmdZwdtmdvwMZQff',
'DRVjcqhRchhGGllhCgdGQQzfttzGQGwQfg',
'cDRljchpqTcjDFTFVcPcPCWBHpNnJNNSnbWbHHrSpWHr',
'dtHrRrBHrCRhddftjgBrRhgjsbbbMpbSWSTjWcsDTWDbcW',
'GQPFVQVQnJlqVMDcMzpDfzpDVD',
'qZZJFLlLnvFFGPGLPqnJvwQldfgHrBRBmBhgNBRHghNhhwRg',
'rLbrZhPgqZhMdVFSFTSGCqFG',
'zsszfRzjtHtzvRTSDdFFCtdDdtND',
'fcwllfmwzRHlfmmzFvQQLrgLMLBZhJQZPrZhJLhW',
'sllrCfpQQJpMHLgzwDwpNqzzVDpV',
'RZPFZPGcSMFtGPRGMwNDVwdRgzvNwgqNvg',
'hBmbMcBmcThmcGtSFTZfQCJjrHLJfsjhWJssJl',
'DqGCbGfCRhfZCVbbqDJJGJBgRNpNdpBNNgNBBNwHnRgt',
'rcWSsSSPSQtwBwHD',
'MLscLMzvvTvcTLzvWWFDPTTrGqmFGGqCZJGbblbVbVZZVmFJ',
'FprpsLQTrstQHNmVSVml',
'JMggWPggWcRbwgJPCGMcGcfmzHlMNSjfzVNhHfVtzSMz',
'cwnPnBwgnGRgRCgRbWJLpFsLtFBLFrDLFZZDrL',
'lVgjLLLMgFMDCwCFqCRbngsvnGSvnSGndbsfgf',
'WZJcTWcNTmJZphmTJJNQHcdvfdbvnRRGbGthdrbttfSv',
'ZPQTJTpTNPJNQTmJRBZJNBHjwMVwPCMwVlVzjwwzqqjVjL',
'hznNhNQNQFDWVFmDQm',
'SMqZBMMbBvDbHPzzdVPH',
'zzzTBTMLNTgpnTTh',
'NLCdmsdCVLGHCHdQzzmznnFwRjFMDMwpTBjDRpnpTBMJ',
'PrcfcrglcfWbSqgrlqvShrwpJpDBFJHpBWjTDTRTRTTB',
'crSgSHtPttfdLGmtzzZNNV',
'BTlTVqCBqtTcBqVhWlsJjDvsnLsvlvpJPj',
'gMgggGZbSMzNRRRLmZZnQZQPPDvnsnDvJwwQ',
'dMRRmMgbNfRgmfSdGFgNgTBtrhrhqfWtLCCWLTWWHc',
'zcfVrPwnwrPmrvnjdFdBbHFFdd',
'CCqpSSQQpQZLDCSHPpBFvFBjTHRvRR',
'DMLGthLZMLtQGhGNMPqGSDflzfwcVmzJzsfgNVrswcrr',
'hSgvMTQvChSqPvhTrRLlVHJgfgRJlHHHJH',
'jmzsZzZzwmmLGGtwtVJWNNDRDtVcfVRl',
'GnBBLbzzzFszBFpzvSdrQQCTCQbhMvSQ',
'VHpTMrZMMbDbbpTZmQmTnmzhTqjqlWWQ',
'GGvgNsvNCNvvGvlqqdzWZmlsmZqZ',
'wNNNgccNGJSNBSRNBNvNcvJHLDDZMFRMppMLrfHDLbrrHF',
'spssbPMLpPllspGNsNWMrnwddnfcqrnwwwwMwM',
'VmQBFCjzzjmfnwbrngcVrd',
'FQbSFjBvvzsWvWGlvWNl',
'JLFSwfwRLLfGhnQJBQshvn',
'pZgNcpCWpWtcvhjGGjtVvszD',
'CccMcPcgTTCWmcZcWMcmTNZPmHdrqSHFRRrqwrSrRqwrHmsH',
'BPMhflJRhqnPNGjNRNRjgSRm',
'VdVsDswTVZbCwCZBrcDCczTwtjtNNjmjmgpmjpQggpGVSgQm',
'sTbWrsTBbrTPPnqlJnPPhW',
'nvrgjMWBvQWPvQnsZfGcZcRFdGFtdtZB',
'bHVDwmqNNDhHNzqpphLNHVLpSJcdZtfffRZdDgRFGSddcRZt',
'HNLNqNqLNbhqVVbClngjnQWPTWgsCgvT',
'tfstpcScscBTFTpFnsWSmgdzJlgmgBmPPzJmvdPm',
'jnrqrLHRwGrwhdPvvPvhjJmP',
'qqCLRCGrZZqCHRVtVWQptFWppnbcWb',
'wCDJZJgDwHpdqHhdGHBhhH',
'WSPmJMlmbSmztQlQsvPhnhGGdBddBqdGddTbVB',
'WzWQftWMSWtmvmmSWtMQPgggpZwLwZjggJFgrpFCfj',
'MvQBJMBQhjQFNFnjnj',
'dtlZmRtLmjSTSLLtTtNVwWzDRzDVwwWFwnNn',
'dmmLCqTdcLqtLGqjBhpfHqBGpv',
'PBPRhjTPPlLRBvlvfwffqJGfpG',
'rHtMtrszFtSgbFrrggrFgMnwWGzmQqWvGWzGQpJGfNqqNz',
'FggcbSMntVgMdRCwZcjChLCT',
'lCqqBlCwlnDqPZTZZBLNdjJLwttNWjjdzJzc',
'fVfMbvbvmbVsmSsmMVWNtzzcjgLWgjztMMtg',
'VVmFhFRSfbQsvVQmvSfhSsmzHlCZqrrBrDBrHZPRTZnnzB',
'CRrDWmzRRQMmDqrrBgBQmtHljhHwtwlwplcBjHGwwB',
'PWfPSWnvsNZSZdfjHjZtGHjchllltl',
'WVsnbSPTbNdbmqTQmmrmLzTq',
'cGtMBGSJDgtgMBsBMgMvWWSHWjpjzHTWTPpqWzqW',
'mNVQNsdVsdhLmCpTWWjmCjTT',
'NQQwrfbQrNQNbrrdLwfQsZdgFbBBFBgggRGRDMRFFMRDgM',
'lFnqgqWQvHWqgvlVglvqjPjcLdfLfBPLnrbLNLcN',
'hmTmthppsRtpTRRTZMpSbLdNjNcJLcrcBNbJBZZc',
'smmpRsTtpSSsRGhppmmhdCMGWwqFQgWGWWDgWwVFHQqHgg',
'mWFjmcdcFWcSSQjzrpvrwRGvTwQGGG',
'HRJfgMZVhtRlHJHBVJTGvGppbpbvvGTvTtrv',
'glsgVMVqffdnPRDcqLnL',
'MtvLJdmLLTvSSCtSzLSTcDhRjRftQjjssshfQNjPtf',
'nlggrFWzRsfFjVQN',
'WgwwBgbgZBHGBnccTzMCLTZJmLLL',
'sRtHTBBHZtDTtZhdPzWdGcdVFdJmGcnm',
'wpwMLWCgvfNvwvwbbCrwgfzPncrJPSFVGPnrcJSVznmV',
'bLpvwQwMwpjWMgfvgZTsDsBttqHRjTqHlH',
'mpmGpCpmlpmwfmCQVppCVfQSSjvSqgWvvvDgNwWDgnnDnW',
'RBLsHRJBRrHJWFDWSNqFWj',
'zZBLdsdcZrsBjGfpGVpTTPGlVc',
'NBbTzgwSNmrFWpVrzrFM',
'LnZQtQlZVnMrFBBG',
'CCdtddBtPdNqcvHSCCcg',
'ZFbZPHbZPTQVVlsGNF',
'qtvDWvgRftqGNccCNVThDs',
'fRwGBBjBppdMdBMZ',
'GffflsZsPZVfjsssNfZsJNNZVcMDSqMWFcwFMMpcTMTTFSTS',
'LhrCmvzcRbbhtmRdTCMDwWMpDWqqqMpW',
'dvRQmBBvLzBRRvRhhcdbhdRgjHQNllJsfsNlZZljZGGNQN',
'wjbMPsbfLzVCTMVbjLplmpshhSpHShhJhtsm',
'ZrcqZTDTGDqFdJtGmdGSpl',
'QNNrWvQRqRNWnTQRvqjPbjfWbCBCMbMLBwMV',
'wRPRsppFfWJRlPRPFlpJfwSMzzZTBwBtZTTCMCMtdz',
'vGLGrjcfrLVGjfnGTMCMtNNnCTnMtCBd',
'VrjqhjhLVcrGVRqJmqQspmfFWm',
'LRfdnmwMwdSBmfvJNrrgLhCNgqqJWs',
'llctPPVTcPStgJgshCsrCs',
'DpTlFpFVRFZRFFSv',
'sPgRgsmdcqmgSvvFRRRRdqdFfTWZhhdZrZbbWfTpwDfbWTbw',
'jLCCHtLljJzjlplfZSlwTfprZZ',
'tBHVjQHzHQJBtSVmvRsvvFRqnGgv',
'spppVDbVcbgVSFgFZZbGZgbJMRBTvHTvJJHGtHRwtMGvHT',
'LldflzQLLQmQWQQfnwMWwHJtTtwRBcBt',
'CPjfhCmNmNfFVchpchFVhp',
'bZQJgQmQmTgnLBRtNPNnml',
'ccszcqldGzhszrVsqdlHVNwLpppwHPHRtBBppDNRLt',
'VSzVhVdcfrrhcqGrVhrssQQlMbJvFjMgbFSQggCvCv',
'hHWVWhhlZDZVWNTgczWLjbtcTFFj',
'JJnPnCdBCBnnRCjSsjStBgsbFttb',
'MRpgCpGqdPRppJwpnRqRfZZhmvhHDrhllDHhhZGZ',
'SPcgLDcLLnWFWCNVCRPT',
'fhZQtsbtmbmfZTVTVRWfNvTCTT',
'jhbbmzRsQzpLDcgLHLjg',
'GSFRHrCCGRJDJtrgWdrL',
'stcVQshQZBsBmjMsZhmMQQWDDvNWdncNWvzLgdDnzdDN',
'sVwMBQBhVVjtQZVPlSfPCfwRpSCpRl',
'bBHHJMJvBvWMJWqqccNNPhMCrclChQCC',
'RPppPgfpwgmcQgrhmm',
'tfwTwpFPGGwZSRtpVjJHbHLvSvLSqVLL',
'jlJfZGjljJPBqJGnfGVMqGfrFWWddvDmFRDcmdFDdDvbDM',
'hTCTsgsgwhTbvRdcFmsddpFd',
'wbQNHTQLgCwSThhCgwnZnJfqnqJBlNlBnnVl',
'CLlfbjjbLlbbDGbLzfCGhdtdWBthdBWsHvWHBnntWs',
'rmJRJFqrDwVFTwFmSJvtvMtdJMMHBdBBndWt',
'ZVrVVZpgTpZFSqmZqRNlNNfQQbpGjDQbbpPl',
'mVCrhGHGmZhrNlDwbWnLWWvGLWWwnd',
'PNsqgzspsgNFJNFfzqpWSWdwSvSPnvdWbSbvjd',
'NzgJzqMcgscQqJcpJRzBmlrBRBDDlHZBBBHtHZ',
'NJmNJDwcMmJNMbJJDNDqcGcsWRWHQzRPQjZLRGZWLQsjZQ',
'dgSnTBgdpddtgShSTZjLRhRLHqWPPhPRPQ',
'VgdTpBntlvBVrlfcbqJcMrfmcqmb',
'wvqwvPwNJgFmLdvDJFDmDLvJlQZpMzSpBVflpdSSMlQnfldS',
'WjCcRZCWRjjRtsZhRRhpSVBVnzplBfWnfBfSQz',
'CbRbcsjHZrhbTRtsGbCrgNgDDPFFqvvJvJFDFw',
'GlsCrbCChShqgqlbSCcVbqgVhBwjBDFBhBhdDWvwBFFvWvDv',
'THmHMmtMnLfHRnzRZnfLBDWWsWzWFNsvWjjvjvFF',
'mpHRtmZffHTTMpmLMLLnJtJCgScScsPlblcpCrPbblCPlq',
'vscDLrcvrsLNStdTfBCvgJTqGBdd',
'bwLbzRhbbdTfbgCB',
'pplQzLwmPZVMStcDjFtQrS',
'RMjCrhFJhRVRVCCFFsvmnvqrmbvqmqSmbrvm',
'tzfpBgTHzttGzZpBfHGDBZHbccnGqbmvdNlGnSnlcvSwbn',
'pDWTHDTzgTfWZpVVsWSPjRFSMsFs',
'fmrfmrwVfjmrzjqCsqqvjsvvpG',
'hFDVtFStVtJnPPtJNHbtQWGbQsCvCsQgpWGggdQC',
'NBSDSNHStHNHnhStHNNrcflrmTzBlwmzrlMVVw',
'SjtZZSdNcDldPQqndl',
'BbgzgWgTmTBfwrbnDjQDwVPwDlnsVq',
'zBBrCTTMBWLMWmfMfbbmrMtjNZLFJRRZSSvFFtStvGGJ',
'CTCGLGCFRRSMGnZnLCTfdffhpbNbDfpdZBvhdv',
'rJlqclVPHJWVrgPPQqjqgJlhBhDBBQdvbhwvNfhswfNpvb',
'tltrcrHjlVWVCDzSGCCzLCGt',
'sbHHsbCCHbLSVfJbbfSLNJBzvzMMPrhPPNztZlZNZhdt',
'GTWjplTgDnGmQGpQnQhZrvvBMPztPzvrzvjZ',
'mQgGWllcFcTFmgwcDppDQGTCqfsSLqsfSbqJqLSSFsbRfF',
'jslsFjLLLLvFwWtQFTFDJQWp',
'dGzdrNmRWqVBGcTbwpRDRnbJDRhT',
'qzqzrrPNNrmfLPsjglHjgW',
'QjCHcPfcgQSgPPcffQSmmmLmrJJpNpBMrJMtFrBBBMFrrpNS',
'VGVZfDbbVVZWGvDbFrlBZNJBNlNMwwtM',
'sbvfhqTGTRnhTVGvzgHmgQLQmPqzmPLm',
'sLwnMHnbnLMjGpZsjGGtpc',
'ggvJrNNTQgQrNvgqBqZCCjClWjGtWjCpGJFW',
'TVdrqvVrTNTzBqQQzTRMfHbMwMbZMdMbHwRD',
'bcfJQQJHsQPCpdpWdPbb',
'RHjHDwZtrZmRDDtwtjRBVFdWVrrrBClldVphCF',
'zDgwgNzjmDnMnzMMHncG',
'vMHRvMhvHWRBRDHhRBwWvRBqLqbGwqnqnnNTbNqdNbbVVr',
'pslgcZszJltrsZcZgNnnqbSSTSSndbNbzS',
'cZcgsZgZZgPgmcpfJtfttWBQvmFWjDQDhBmFjDHvFr',
'bVbBvdTTVLbCgCznLJsJcwHPczfz',
'NFcDphSDrFjGtZNZjplZGZFnzPHPrzHHzJMnnwfPsPsRJs',
'cGtGljFmWdvqmVCV',
'qSNbTvcvTGTvGcgtBNvcbdrdjrnjRnjRVHdDqHrRHj',
'ZZZZPLWPzPDCCsCRnRdwVFnjdwPVFP',
'ChlCLLZftfcBvfDv',
'cRtfctVgmRclmBFGbbMBDDFPtD',
'svQZhHSHssjTvjpQjSSBBMJMJGDBpPbMzzpGzP',
'ZsvsCTWhCHhSwwjrwbndldlRnfRNmb',
'PQdTgdGpRcTccCfj',
'hHFLHlHBhBlmlDFzHrhhfZNZbfNZcVWNVVZRDjCC',
'LFLLMHJHSBhBFGGnMMvsGtGGtj',
'fwmVnVCDVqpNQqqb',
'ddBcZZWdvGWzBzsWvLvddlNHcHQPbQqqJQNNQHPHQT',
'WgGvsMMzvgbntDhCmt',
'JjwhFMmwjJwmCgTgSCSFlPLg',
'WWbsbVtftBZWtnWtncbQvctTGLpLgCpzPPPlllpzlgPPTQ',
'TBvnfBffWsfVtTvbZBTNjwjqddhMNqwRMMhdRMrq',
'SllrbtTSQrSQrbrvvMvzFDsBsssWpWdWbGpGBWNWNW',
'hhCfmmmjmPLCfmnPLfqPgqqNNBpjZBZQDNQdpWNpdBBsBp',
'RhLfPhQLQfCRnHfqTHHrFJMrttTwTtzt',
'BFrFBJMMJnnsNJBFCdLCnmvzbPdCmPnc',
'LDLVHQRfDvdHdcCmcv',
'llQDwqSVLwZLZSgsGZMNMgTjTMTr',
'mrwdbqRhdCNGgZBHbH',
'jVTPMjvjpvMfTfQfPlpHHZNnNBHgZDGsGMnCsZ',
'TLlfQpffQvvzhtNqztRFtzcm',
'DDfvJZZPDHVPSPcSvcgcWCsWQcTTdhQTTh',
'dMwpbdjRtrFhhTsTFQWqhC',
'bGRdNpbzlvLfDfZlLZ',
'bdPQdcpdbpjFqpQcQwqqhhNRhJvWRfrrWBsJrfwN',
'mMtlZfmtnLZtSnGDlmGWRRhrWLhJsBRvgRWghh',
'DnMGCtmCzfGMbjdQbVzpqcFH',
'jwnGggRBvvpBZCljCsCWrhhrsh',
'FVMcFLqLMqcJfVtDqMJcHMHWCSblzzrWsdhSLlSzbrGCLz',
'HQVFPDtDQDFFNTZpPgNnGgNn',
'HNBHNqlqHJQBRNvdmZvmPdZZlpnT',
'bDbbhDgSfzVVfnvPmfHmTZZd',
'jgzbwrhVsDgsDWLwJqqBMqcqHL',
'tzNtJzsJVBHzbjbglCHc',
'nfmnGnmPhntCgHvtvmCj',
'MStTwrMTWrTdBZSNLZJNVQ',
'NVjmwmVGGwGFHstwFHMhTh',
'psRSzzscZscZpgQQzqQtBBHTTlThHHtTTh',
'rCprbpZccggcrRzbbRRbscvVVWWvNfvVWnGDCWVNddmd',
'rphfGDgtPtllrPlFlGrhGjnmnTnjcBsncBBVpTTBmc',
'SqqZMJCLwgCwJgQRqqgZQNwdBBsBBHVBdTHNsnVNBTccnc',
'MJqZZMbqgzRCSJZwPtFfGzWhrrfGttWl',
'cSZqqcwbqVzqCbqVqVZPsvvDCDrffngvphggndhdGh',
'tTNTMWJNQJHMNGSSprfdGnfdth',
'WNRHWWMJSRWzswbczsVPRs',
'HCgcSMhSMBGMdvGf',
'RNQqbDQqFdRFdmTZfGtPZvtGlQffll',
'mNpdNrRDbTNrmbpzmpWmbpWcswhcHcjhscSHjSgVHwHn',
'MwgcFgwMMcscCbMFsMFCgMgPPLWPvptvBvPvtvvWmBBzwG',
'nhQQjTJRVDdQJrPpmnGGBmvtGvLz',
'HdJQdJHjrJQDBQjhQVQJhdJcqlFHcSqsNbCbCqCHFqCFgC',
'JvTnvWtdJLbhJHbMwwHjcGHCwHwQGQ',
'mqtmsllmfqVFwMwMrrPjmQrC',
'lfztRZSlRDRVzfdpWnSvWhNdbnpp',
'rSvrgggzHTNzrHtnptpmlDngZjWj',
'MdMhqMhsfMSRcGqRsQQRctjjdDnjtjClCjjpZnDlnt',
'BBMRsQRfRcscGqBfRRsBssPBLLzNLFPwvVFFPTLbbLwHHTvS',
'pCmCfdPFzmsFsDhFFDsttptpRtJjLnlJRtttHt',
'ZQwgWZgqJhTTRtgV',
'GNqWNvcqqQQrMMWcQzDDsSzBDBSssSmhhr',
];

let fullResult: Length<Result<Badges<FullInput>>>;
