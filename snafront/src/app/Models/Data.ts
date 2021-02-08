export interface Data {
    time: number;
    movies: string[];
    rmsa: number;
    accuracy: number;
    f1_score: number;
    precision: number;
    recall: number;
    rms: number;
    error?:string;
}