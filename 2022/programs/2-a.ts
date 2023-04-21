type Length<T extends unknown[]> =
  T extends { length: infer L } ? L : number;

type BuildTuple<L extends number, T extends unknown[] = []> = 
  T extends { length: L }
    ? T
    : [...T, ...T] extends { length: L }
      ? [...T, ...T]
      : BuildTuple<L, [...T, unknown]>;

type Rock = [unknown];
type Paper = [unknown, unknown];
type Scissors = [unknown, unknown, unknown];

type A = Rock;
type B = Paper;
type C = Scissors;

type X = Rock;
type Y = Paper;
type Z = Scissors;

type OutcomeScore<Them extends unknown[], Me extends unknown[]> = 
  Them extends Rock
      ? Me extends Paper
        ? BuildTuple<6>
        : Me extends Scissors
          ? BuildTuple<0>
          : Me extends Rock
            ? BuildTuple<3>
            : never
    : Them extends Paper
      ? Me extends Rock
        ? BuildTuple<0>
        : Me extends Paper
          ? BuildTuple<3>
          : Me extends Scissors
            ? BuildTuple<6>
            : never
      : Them extends Scissors
        ? Me extends Rock
          ? BuildTuple<6>
          : Me extends Paper
            ? BuildTuple<0>
            : Me extends Scissors
              ? BuildTuple<3>
              : never
        : never;

type TotalScore<Them, Me> = 
  Them extends unknown[]
    ? Me extends unknown[]
      ? [...OutcomeScore<Them, Me>, ...Me]
      : never
    : never;

type ComputeRounds<Rounds extends Array<[unknown[], unknown[]]>> =
  Rounds extends []
    ? []
    : Rounds extends [[(infer Them), (infer Me)], ...(infer OtherRounds)]
      ? OtherRounds extends Array<[unknown[], unknown[]]>
        ? [...TotalScore<Them, Me>, ...ComputeRounds<OtherRounds>]
        : never
      : never;

type ExampleMatch = [
  [A, Y],
  [B, X],
  [C, Z],
];

let testResult: Length<ComputeRounds<ExampleMatch>>;

type M1 = [
[A, Z],
[B, X],
[A, Y],
[B, X],
[C, Y],
[C, X],
[B, Z],
[C, Z],
[A, Y],
[C, Z],
[B, Z],
[B, X],
[B, X],
[C, X],
[C, X],
[B, X],
[B, Z],
[C, X],
[B, Y],
[B, Z],
[B, X],
[C, Z],
[A, Z],
[B, X],
[A, Y],
[B, Y],
[C, Y],
[B, X],
[B, Y],
[B, Z],
[B, Y],
[B, Z],
[A, Y],
[C, Y],
[B, X],
[A, Z],
[B, X],
[C, Y],
[C, Y],
[C, Y],
[A, Y],
[B, X],
[B, Y],
[C, Y],
[B, Z],
[C, Y],
[A, Z],
[B, Y],
];


let r1: Length<ComputeRounds<M1>>;