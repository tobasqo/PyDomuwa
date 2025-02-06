import { z } from "zod";

export enum GameTypeChoice {
	EGO = "Ego",
	WHOS_MOST_LIKELY = "Who's Most Likely",
	GENTLEMENS_CARDS = "Gentlemen's cards",
	NEVER_HAVE_I_EVER = "Never have I ever",
}

export const GameTypeCreateSchema = z.object({
	name: z.nativeEnum(GameTypeChoice),
});
export type GameTypeCreate = z.infer<typeof GameTypeCreateSchema>;

export const GameTypeUpdateSchema = z.object({
	name: z.nativeEnum(GameTypeChoice),
});
export type GameTypeUpdate = z.infer<typeof GameTypeUpdateSchema>;

export const GameTypeSchema = z.object({
	id: z.number().min(1),
	name: z.nativeEnum(GameTypeChoice),
});
export type GameType = z.infer<typeof GameTypeSchema>;
