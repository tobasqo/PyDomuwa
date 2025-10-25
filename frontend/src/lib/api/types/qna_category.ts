import { z } from "zod";

export enum QnACategoryChoice {
	SFW = "SFW",
	NSFW = "NSFW",
}

export const QnaCategoryCreateSchema = z.object({
	name: z.nativeEnum(QnACategoryChoice),
});
export type QnACategoryCreate = z.infer<typeof QnaCategoryCreateSchema>;

export const QnaCategoryUpdateSchema = z.object({
	name: z.nativeEnum(QnACategoryChoice),
});
export type QnACategoryUpdate = z.infer<typeof QnaCategoryUpdateSchema>;

export const QnACategorySchema = z.object({
	id: z.number().min(0),
	name: z.nativeEnum(QnACategoryChoice),
});
export type QnACategory = z.infer<typeof QnACategorySchema>;

export const QnACategoriesSchema = z.array(QnACategorySchema);
export type QnACategories = z.infer<typeof QnACategoriesSchema>;
