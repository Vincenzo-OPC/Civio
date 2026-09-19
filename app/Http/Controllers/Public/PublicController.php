<?php

namespace App\Http\Controllers\Public;

use App\Http\Controllers\Controller;
use App\Models\LegalContent;

class PublicController extends Controller
{
    public function welcome()
    {
        session()->forget('is_free_attempt_active');

        return $this->render('public/welcome');
    }

    public function about()
    {
        return $this->render('public/about');
    }

    public function support()
    {
        return $this->render('public/support');
    }

    public function guide()
    {
        return $this->render('guide');
    }

    public function privacy()
    {
        $privacy = LegalContent::where('type', 'privacy')->first();

        return $this->render('public/privacy', [
            'privacy' => $privacy,
        ]);
    }

    public function terms()
    {
        $terms = LegalContent::where('type', 'terms')->first();

        return $this->render('public/terms', [
            'terms' => $terms,
        ]);
    }
}
