// Resolves to the length of a tuple type T
type Length<T extends any[]> = 
  T extends { length: infer L } ? L : never;

// Resolves to a tuple of length L, with elements of type any
type BuildTuple<L extends number, T extends any[] = []> = 
  T extends { length: L } ? T : BuildTuple<L, [...T, any]>;

type Add<A extends number, B extends number> = 
  Length<[...BuildTuple<A>, ...BuildTuple<B>]>;

type Subtract<A extends number, B extends number> = 
  BuildTuple<A> extends [...(infer U), ...BuildTuple<B>]
      ? Length<U>
      : never;

type Equals<A, B> =
    A extends B
        ? (B extends A ? true : false)
        : false;

type AtTerminus<A extends number, B extends number> = 
    A extends 0
        ? true
        : (B extends 0 ? true : false);

type LessThan<A extends number, B extends number> = 
    AtTerminus<A, B> extends true
        ? Equals<A, B> extends true
            ? false
            : (A extends 0 ? true : false)
        : LessThan<Subtract<A, 1>, Subtract<B, 1>>;

type Max<A extends number[]> =
    A extends [infer X, ...(infer Ys)]
        ? X extends number
            ? Ys extends number[]
                ? (LessThan<X, Max<Ys>> extends true ? Max<Ys> : X)
                : never
            : never
        : never;

type Sum<A extends number[]> =
  A extends []
    ? 0
    : A extends [infer X, ...(infer Ys)]
      ? X extends number
          ? Ys extends number[]
              ? Add<X, Sum<Ys>>
              : never
          : never
      : never;

let tuple: Max<
  [
    Sum<[1, 2, 3]>,
    Sum<[4]>,
    Sum<[5, 6]>,
    Sum<[7, 8, 9]>,
    Sum<[10]>,
  ]
>;
