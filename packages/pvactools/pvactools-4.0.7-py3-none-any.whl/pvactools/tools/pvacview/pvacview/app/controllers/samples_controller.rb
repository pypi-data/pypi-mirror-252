class SamplesController < ApplicationController
  before_action :set_sample, only: [:show, :edit, :update, :destroy]

  def index
    @samples = Sample.all
  end

  def show
  end

  def new
    @sample = Sample.new
  end

  def create
    @sample = Sample.new(sample_params)

    if @sample.save
      redirect_to samples_path, notice: "Sample was successfully created."
    else
      render :new
    end
  end

  def edit
  end

  def update
    if @sample.update(sample_params)
      redirect_to samples_path, notice: "Sample was successfully updated."
    else
      render :edit
    end
  end

  def destroy
    @sample.destroy
    redirect_to samples_path, notice: "Sample was successfully destroyed."
  end

  private

  def set_sample
    @sample = Sample.find(params[:id])
  end

  def sample_params
    params.require(:sample).permit(:name)
  end
end
