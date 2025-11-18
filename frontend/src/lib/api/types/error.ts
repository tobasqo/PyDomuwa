import z from "zod";

export const ApiErrorSchema = z.object({
    errors: z.array(z.unknown()),
    statusCode: z.number().min(100).max(599),
});
export type ApiError = z.infer<typeof ApiErrorSchema>;
