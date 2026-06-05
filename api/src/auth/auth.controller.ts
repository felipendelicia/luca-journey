import { Controller, Get, Req, Res, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { Response } from 'express';
import { Public } from './public.decorator';
import { CurrentUser } from './current-user.decorator';
import { AuthService } from './auth.service';

@Controller('auth')
export class AuthController {
  constructor(private auth: AuthService) {}

  @Public()
  @UseGuards(AuthGuard('google'))
  @Get('google')
  google() {}

  @Public()
  @UseGuards(AuthGuard('google'))
  @Get('google/callback')
  async callback(@Req() req: any, @Res() res: Response) {
    const { googleSub, email } = req.user;
    const { token } = await this.auth.loginConGoogle(googleSub, email);
    const front = process.env.FRONTEND_URL || '/';
    const base = front.endsWith('/') ? front : front + '/';
    res.redirect(`${base}#token=${encodeURIComponent(token)}`);
  }

  @Get('me')
  me(@CurrentUser() userId: string, @Req() req: any) {
    return { id: userId, email: req.user?.email };
  }
}
