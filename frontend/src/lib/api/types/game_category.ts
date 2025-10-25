import { z } from "zod";

export enum GameCategoryChoice {
	SFW = "SFW",
	NSFW = "NSFW",
	MIXED = "MIXED",
}

export const GameCategoryCreateSchema = z.object({
	name: z.nativeEnum(GameCategoryChoice),
});
export type GameCategoryCreate = z.infer<typeof GameCategoryCreateSchema>;

export const GameCategoryUpdateSchema = z.object({
	name: z.nativeEnum(GameCategoryChoice),
});
export type GameCategoryUpdate = z.infer<typeof GameCategoryUpdateSchema>;

export const GameCategorySchema = z.object({
	id: z.number().min(1),
	name: z.nativeEnum(GameCategoryChoice),
});
export type GameCategory = z.infer<typeof GameCategorySchema>;

export const GameCategoriesSchema = z.array(GameCategorySchema);
export type GameCategories = z.infer<typeof GameCategoriesSchema>;
