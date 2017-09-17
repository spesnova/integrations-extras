require 'ci/common'

def spinnaker_clouddriver_version
  ENV['FLAVOR_VERSION'] || 'latest'
end

def spinnaker_clouddriver_rootdir
  "#{ENV['INTEGRATIONS_DIR']}/spinnaker_clouddriver_#{spinnaker_clouddriver_version}"
end

namespace :ci do
  namespace :spinnaker_clouddriver do |flavor|
    task before_install: ['ci:common:before_install']

    task :install do
      Rake::Task['ci:common:install'].invoke('spinnaker_clouddriver')
      # sample docker usage
      # sh %(docker create -p XXX:YYY --name spinnaker_clouddriver source/spinnaker_clouddriver:spinnaker_clouddriver_version)
      # sh %(docker start spinnaker_clouddriver)
    end

    task before_script: ['ci:common:before_script']

    task script: ['ci:common:script'] do
      this_provides = [
        'spinnaker_clouddriver'
      ]
      Rake::Task['ci:common:run_tests'].invoke(this_provides)
    end

    task before_cache: ['ci:common:before_cache']

    task cleanup: ['ci:common:cleanup']
    # sample cleanup task
    # task cleanup: ['ci:common:cleanup'] do
    #   sh %(docker stop spinnaker_clouddriver)
    #   sh %(docker rm spinnaker_clouddriver)
    # end

    task :execute do
      exception = nil
      begin
        %w[before_install install before_script].each do |u|
          Rake::Task["#{flavor.scope.path}:#{u}"].invoke
        end
        if !ENV['SKIP_TEST']
          Rake::Task["#{flavor.scope.path}:script"].invoke
        else
          puts 'Skipping tests'.yellow
        end
        Rake::Task["#{flavor.scope.path}:before_cache"].invoke
      rescue => e
        exception = e
        puts "Failed task: #{e.class} #{e.message}".red
      end
      if ENV['SKIP_CLEANUP']
        puts 'Skipping cleanup, disposable environments are great'.yellow
      else
        puts 'Cleaning up'
        Rake::Task["#{flavor.scope.path}:cleanup"].invoke
      end
      raise exception if exception
    end
  end
end
