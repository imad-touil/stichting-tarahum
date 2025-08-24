<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        // If you already have the users table, skip creating it
        if (!Schema::hasTable('users')) {
            Schema::create('users', function (Blueprint $table) {
                $table->id();
                $table->string('name');
                $table->string('email')->unique();
                $table->string('password');
                $table->enum('role', ['admin','case_manager'])->default('case_manager');
                $table->timestamp('created_at')->useCurrent();
                // No updated_at because your existing table doesn't have it
            });
        }
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        // Only drop users table if it exists
        if (Schema::hasTable('users')) {
            Schema::dropIfExists('users');
        }
    }
};
