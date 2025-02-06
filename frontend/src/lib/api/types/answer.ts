import { z } from "zod";
import { PlayerSchema } from "$lib/api/types/player";
import { GameTypeSchema } from "$lib/api/types/game_type";
import { QnaCategorySchema } from "$lib/api/types/qna_category";
import { QuestionSchema } from "$lib/api/types/question";

export const AnswerCreateSchema = z.object({
	text: z.string(),
	authorId: z.number().min(1),
	gameTypeId: z.number().min(1),
	gameCategoryId: z.number().min(1),
	questionId: z.number().min(1).optional(),
});
export type AnswerCreate = z.infer<typeof AnswerCreateSchema>;

export const AnswerUpdateSchema = z.object({
	text: z.string().optional(),
	excluded: z.boolean().optional(),
	gameTypeId: z.number().min(1).optional(),
	gameCategoryId: z.number().min(1).optional(),
	questionId: z.number().min(1).optional(),
});
export type AnswerUpdate = z.infer<typeof AnswerUpdateSchema>;

export const AnswerSchema = z.object({
	id: z.number().min(1),
	text: z.string(),
	excluded: z.boolean(),
	deleted: z.boolean(),
	author: PlayerSchema,
	gameType: GameTypeSchema,
	gameCategory: QnaCategorySchema,
	question: QuestionSchema.optional(),
	prevVersionId: z.number().min(1).optional(),
});
export type Answer = z.infer<typeof AnswerSchema>;
