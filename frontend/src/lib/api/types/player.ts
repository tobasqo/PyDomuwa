import { z } from "zod";
import { UserSchema } from "$lib/api/types/user";

export const PlayerCreateSchema = z.object({
  id: z.number().min(1),
});
export type PlayerCreate = z.infer<typeof PlayerCreateSchema>;

export const PlayerUpdateSchema = z.object({
  gamesPlayed: z.number().min(0).optional(),
  gamesWon: z.number().min(0).optional(),
});
export type PlayerUpdate = z.infer<typeof PlayerUpdateSchema>;

export const PlayerSchema = z.object({
  id: z.number().min(1),
  user: UserSchema,
  gamesPlayed: z.number().min(0),
  gamesWon: z.number().min(0),
});
export type Player = z.infer<typeof PlayerSchema>;
